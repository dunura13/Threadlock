import os
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from supabase import create_client

load_dotenv() 

try:
    #test openAI connection
    ai_client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

    # test supabase connection

    supabase = create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY")
        )

    print("Keys are working")

except Exception as e:
    print(f"Error loading keys: {e}")

# create FastAPI app

app = FastAPI()

@app.get("/")
def health_check():
    return {"status":"alive", "message":"ThreadLock is running"}




