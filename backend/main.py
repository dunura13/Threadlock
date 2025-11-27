import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks
import google.generativeai as genai
from supabase import create_client, Client
from slack_sdk import WebClient
import json
from jira import JIRA



load_dotenv() # load environemnt variables


# initalize supabase 
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



slack_client = WebClient( # initalize slack app
    token = os.environ.get("SLACK_BOT_TOKEN"))

# configure gemini
genai.configure(api_key = os.environ.get("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# JIRA initalization
jira_options = {'server':os.environ.get("JIRA_URL")}
jira = JIRA(
    options = jira_options,
    basic_auth = (os.environ.get("JIRA_EMAIL"), os.environ.get("JIRA_API_TOKEN"))
)



app = FastAPI()

# runs after server replies to slack
def process_decision(event: dict):
    channel_id = event.get("channel") # channel which event occurd
    user_id = event.get("user") # user who mentioned the bot
    text = event.get("text") # text of the message
    thread_ts = event.get("thread_ts", event.get("ts")) # timestamp, if thread_ts is not present, use ts
    
    print(f"AI processing: {text}..")


    try:
        prompt = f"""
        You are a project manager bot. Analyze this message: "{text}"
        
        If a technical decision is made, extract it into this JSON format:
        {{ "decision": "...", "rationale": "...", "action_items": "..." }}
        
        If NO decision is made, return exactly: {{ "decision": false }}
        """

        # CALL gemini api
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
    

        
        # parse result
        result_json = response.text
        result_data = json.loads(result_json)



        # Construct a reply
        if result_data.get("decision"):
            
            # NEED TO IMPLEMENT JIRA CODE HERE
            try:


                data_to_insert = {
                    "slack_channel_id": channel_id,
                    "slack_thread_ts": thread_ts,
                    "decision_text": result_data['decision'],
                    "rationale": result_data['rationale'],
                    "raw_json": result_data # save the full json (jus in case)
                }

                supabase.table("decisions").insert(data_to_insert).execute()
                print("Decision saved to Supabase.")

            except Exception as db_error:
                print(f"Database Error: {db_error}")


            reply_text = (
                f"**Decision Detected**\n"
                f"> *{result_data['decision']}*\n"
                f"**Rationale:**{result_data['rationale']}"
            )
        
        else:
            reply_text = "Analyzed this but didnt find a firm decision. Try being more specific!"

        
        # send reply to slack
        slack_client.chat_postMessage(
            channel=channel_id,
            text = reply_text,
            thread_ts = thread_ts
        )



        print("Reply sent to slack")



    except Exception as e:
        print(f"GEMINI/SLACK error: {e}")
    




@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    # grab headers (check for retries)
    headers = request.headers
    retry_num = headers.get("x-slack-retry-num")

    # parse data
    body = await request.json()

    # handle URL verification
    if body.get("type") == "url_verification":
        return {"challenge":body["challenge"]}
    
    # anti-duplicate logic 
    if retry_num and int(retry_num) > 0:
        return {"status": "ok", "message":"Ignored retry"}

    # handle "App mention"
    event = body.get("event", {})
    if event.get("type") == "app_mention":
        background_tasks.add_task(process_decision, event)

    
    return {"status": "ok"} # so slack does not timeout
    



@app.get("/")
def health_check():
    return {"status":"alive", "message":"ThreadLock is running"}




