Google OpenID Connect (FastAPI) demo

Instructions

1. Create OAuth client credentials in Google Cloud Console:
   - Go to https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 Client ID (type: Web application)
   - Add an authorized redirect URI: http://127.0.0.1:8000/auth
   - Save Client ID and Client Secret

2. Set environment variables locally (Git Bash):

export GOOGLE_CLIENT_ID=your-client-id
export GOOGLE_CLIENT_SECRET=your-client-secret
export SESSION_SECRET=a-random-secret

3. Install deps and run:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000

4. Visit http://127.0.0.1:8000 and click "Login with Google". After authentication you will be redirected to /id_token which returns JSON {"id_token": "..."}.

5. Paste the JSON and the client_id as described by the grader. We (the assistant) cannot log in or obtain tokens for you.
