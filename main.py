import os
import json
from fastapi import FastAPI, Header, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import firebase_admin
from firebase_admin import credentials, auth, firestore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing Token")
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Token")

@app.post("/extract") 
async def extract_receipt(payload: dict = Body(...), user=Depends(verify_token)):
    
    receipt_text = payload.get("receipt_text")
    if not receipt_text:
        raise HTTPException(status_code=400, detail="Receipt text is required")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 

        
    )
        
    prompt = PromptTemplate.from_template(
        "Extract data from this receipt. Missing values must be null. Do not guess.\n"
        "Return ONLY JSON: {{\"vendor_name\": str, \"date\": str, \"total\": float, \"items\": [{{\"name\": str, \"amount\": float}}]}}\n"
        "Text: {text}"
    )
    
    chain = prompt | llm
    ai_msg = chain.invoke({"text": receipt_text})
    
    clean_content = ai_msg.content.replace("```json", "").replace("```", "").strip()
    extracted_data = json.loads(clean_content)

    items_total = sum(item['amount'] for item in extracted_data.get('items', []))
    status = "completed"

    if abs(items_total - extracted_data.get('total', 0)) > 0.05: 
        status = "needs_review" 

   
    doc_data = {
        **extracted_data, 
        "status": status, 
        "userId": user['uid']
    }
    
    
    doc_ref = db.collection("receipts").docume
    doc_ref.set(doc_data)

    return {"id": doc_ref.id, "data": doc_data}

@app.get("/extract/{id}") 
async def get_receipt(id: str, user=Depends(verify_token)):
    doc = db.collection("receipts").document(id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return doc.to_dict()