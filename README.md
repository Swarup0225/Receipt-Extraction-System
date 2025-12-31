# AI Receipt Extractor & Validator

A full-stack application that extracts structured data from receipts using Google Gemini AI, performs mathematical validation, and stores results in Firebase Firestore. It includes a web frontend and an n8n automation workflow.

## 🚀 Features
- **AI Extraction**: Converts messy receipt text into structured JSON (Vendor, Date, Total, Items).
- **Math Validation**: Automatically checks if the sum of individual items matches the stated total.
- **Secure Auth**: Powered by Firebase Authentication (JWT/Bearer Tokens).
- **NoSQL Storage**: Stores all processed receipts in Firestore.
- **n8n Automation**: Automated pipeline to trigger extraction via webhooks.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/))
- A Firebase Project ([Firebase Console](https://console.firebase.google.com/))

### 2. Backend Setup (FastAPI)
1. Navigate to the project folder.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn firebase-admin langchain-google-genai pydantic python-dotenv

### 3.Place your serviceAccountKey.json (from Firebase Project Settings > Service Accounts) in the root folder
### 4.Set your Gemini API key in main.py or a .env file.
### 5.Start the server:
     uvicorn main:app --reload
### 6.Frontend Setup (HTML):
             1. Open index.html.
             2.Ensure the firebaseConfig object matches your Firebase Web App credentials.
             3.Open index.html using a local server (e.g., VS Code Live Server).
             4.Login or Sign Up to access the extraction interface.     
### 7.n8n Automation Setup:
             1.Open n8n and import the workflow.json provided in this repo.
             2.In the Call FastAPI node, update the Authorization header with a fresh Bearer token from the browser console.
             3.Use the Webhook URL to send receipt data externally.     
### 8.Sample Receipt Text: 
             DOWNTOWN BISTRO
             
            789 CULINARY BLVD, MIAMI, FL
            --------------------------------
            DATE: 2025-12-31 12:00 PM
            
            CHICKEN SALAD               12.50
            ICED TEA                     3.00
            CHEESECAKE                   6.50
            --------------------------------
            SUBTOTAL                    22.00
            TAX (0.00%)                  0.00
            TOTAL                       22.00
            --------------------------------
            PAID: CASH


     
   
