import os
import json
import shutil
import requests
import uvicorn
from moa.main import main
from pydantic import BaseModel
from translate import translate_text # G Translater
from disease_cure.main import get_disease_info # Cure for the disease detected
from fastapi.middleware.cors import CORSMiddleware
from inference import get_detections # Disease Detection
from fastapi import FastAPI, Header, HTTPException, File, UploadFile

app = FastAPI(root_path="/farming_tools")

# Configuration
AUTH_KEY = "Asman2010"
UPLOAD_DIRECTORY = "uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

############################################################## Functions ##############################################################

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to restrict methods
    allow_headers=["*"],  # Adjust this to restrict headers
)

class TranslationRequest(BaseModel):
    text: str
    target_language: str

class Query(BaseModel):
    message: str

def verify_api_key(api_key: str = Header(...)):
    if api_key != AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

# Function to print all class names from "Detections"
def get_predictions_class(data):
    for item in data:
        if "Detections" in item:
            for detection in item["Detections"]:
                return detection["Class"]

############################################################## API ##############################################################

@app.get("/")
async def root():
    return {"Hello": "I'm Farming Tools API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/translate")
async def translate(request: TranslationRequest, api_key: str = Header(...)):
    verify_api_key(api_key)

    try:
        full_translation = translate_text(request.text, request.target_language)
        return {"translation": full_translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/farm_gpt")
async def query(query: Query, api_key: str = Header(...)):
    verify_api_key(api_key)

    response, other_model_response = main(query.message)

    return {
        "other_model_response": other_model_response,
        "final_response": response,
    }

@app.post("/disease-detection/")
async def upload_image(file: UploadFile = File(...), api_key: str = Header(...)):
    verify_api_key(api_key)

    # Create the file path
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open("disease_cure/cure.json", "r") as json_file:
        data = json.load(json_file)

    # Make prediction and plot results
    json_response = get_detections(file_path)
    other_info = get_disease_info(data, get_predictions_class(json_response))

    return json_response, other_info

if __name__ == "__main__":
    uvicorn.run(app)
