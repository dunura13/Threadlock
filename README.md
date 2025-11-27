# 🔒 ThreadLock

Turn Slack conversations into tracked Jira tickets automatically using AI.

ThreadLock is an intelligent documentation agent that lives in your Slack channels. It uses Google Gemini (LLM) to analyze conversations in real-time. When a technical decision is reached, ThreadLock automatically captures the context, creates a structured Jira ticket, and logs it to a persistent Next.js Dashboard.

🚀 The Problem
Engineering teams often make critical architectural decisions in Slack threads. These decisions are rarely documented, leading to:

Context Loss: "Why did we choose Postgres over Mongo?"

Zombie Tickets: Action items discussed in chat but never added to Jira.

Manual Toil: Project Managers spending hours copy-pasting chat logs.

🛠 Tech Stack
Backend (The Intelligence)

Python & FastAPI: Chosen for native asynchronous support to handle high-concurrency event streams.

Google Gemini 2.5 Flash: LLM for decision extraction and JSON structured output.

Supabase (PostgreSQL): Persistent storage for decision history and audit logs.

Jira API: For automated ticket creation.

Frontend (The Visualization)

Next.js 14 (App Router): Server-Side Rendering (SSR) for high-performance dashboard loading.

TypeScript: For type safety across the frontend.

Tailwind CSS: For rapid UI development.

💡 Key Technical Features
1. Bypassing the 3-Second Timeout
Slack’s Events API requires a 200 OK response within 3 seconds, or it retries the request (causing bot spam). Since LLM inference often takes 5–10 seconds, I implemented a Non-Blocking Asynchronous Architecture:

The Receiver: FastAPI endpoint instantly validates the request and returns 200 OK.

The Worker: A background task (BackgroundTasks) processes the heavy AI logic independently, preventing timeouts and duplicate replies.

2. Structured "JSON Mode" Output
To ensure the bot never hallucinates or breaks the database, the prompt enforces strict JSON output from Gemini. This allows the system to reliably parse rationale, decision, and action_items programmatically.

3. Full-Cycle Integration
ThreadLock creates a bi-directional link:

Slack -> Jira: The chat bot posts a clickable link to the new Jira ticket.

Jira -> Dashboard: The ticket link is saved to the database for historical referencing.

⚡️ Quick Start
Prerequisites
Python 3.9+

Node.js 18+

A Slack App (Socket Mode or Public HTTP)

Supabase & Jira Accounts

1. Clone the Repo
Bash

git clone https://github.com/dunura13/Threadlock.git
cd Threadlock
2. Backend Setup
Bash

cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
Create a .env file in /backend:

Code snippet

SLACK_BOT_TOKEN=xoxb-...
GEMINI_KEY=...
SUPABASE_URL=...
SUPABASE_KEY=...
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your@email.com
JIRA_API_TOKEN=...
JIRA_PROJECT_KEY=KAN
Run the server:

Bash

uvicorn main:app --reload
3. Frontend Setup
Bash

cd ../frontend
npm install
Create a .env.local file in /frontend:

Code snippet

NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
Run the dashboard:

Bash

npm run dev
📸 Usage
In Slack: Mention the bot with a decision.

@ThreadLock We decided to use AWS S3 for storage because it is cheaper than database storage.

The Response: ThreadLock replies with a confirmation and a link to the new Jira Ticket.

The Dashboard: Visit localhost:3000 to see the decision logged in the table.

🚧 Future Improvements
Slack Home Tab: Allow users to view recent decisions directly inside Slack.

Edit Functionality: Allow users to edit the decision summary before it syncs to Jira.

Vector Search: Use embeddings to allow users to ask "What was the last decision we made about the database?"

👨‍💻 Author
Dunura Epasinghe

