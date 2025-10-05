import os
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"], expose_headers=["*"])

# Session secret (set via env var SESSION_SECRET)
SESSION_SECRET = os.environ.get("SESSION_SECRET", "dev-session-secret-change-me")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# OAuth / Authlib setup
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    # App will run but login won't work until env vars are set
    oauth = OAuth()
else:
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    html = """
    <h2>Google OpenID Connect Demo (FastAPI)</h2>
    <p><a href="/login">Login with Google</a></p>
    <p><a href="/id_token">Show stored id_token (JSON)</a></p>
    <p><a href="/logout">Logout</a></p>
    """
    return HTMLResponse(html)


@app.get("/login")
async def login(request: Request):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return HTMLResponse("Google client not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.")
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as err:
        return HTMLResponse(f"OAuth error: {err}")

    # token is a dict containing access_token, id_token, etc.
    id_token = token.get("id_token")
    # parse/verify id_token and get user info
    try:
        user = await oauth.google.parse_id_token(request, token)
    except Exception:
        user = None

    # store id_token in session for retrieval
    request.session["id_token"] = id_token
    request.session["user"] = dict(user) if user else {}

    return RedirectResponse(url="/id_token")


@app.get("/id_token")
def id_token(request: Request):
    token = request.session.get("id_token")
    if not token:
        return JSONResponse({"id_token": None})
    return JSONResponse({"id_token": token})


@app.get("/logout")
def logout(request: Request):
    request.session.pop("id_token", None)
    request.session.pop("user", None)
    return RedirectResponse(url="/")

if __name__ == "__main__":
    import uvicorn
    # Run the app object directly to avoid import-by-string issues
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)