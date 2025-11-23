import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from openai import OpenAI
from supabase import create_client
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler



load_dotenv() # load environemnt variables

slack_app = App( # initalize slack app
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(slack_app)

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

@app.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)

@app.get("/")
def health_check():
    return {"status":"alive", "message":"ThreadLock is running"}

@slack_app.event("app_mention")
def handle_app_mention(body, say):
    say("Threadlock, at your service!")



