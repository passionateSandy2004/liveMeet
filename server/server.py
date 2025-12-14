from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from livekit.api import AccessToken, VideoGrants
import os
import uvicorn

app = FastAPI()

# CORS configuration - allow Vercel frontend and local development
# Check if we're in production (Railway sets this)
is_production = os.environ.get("RAILWAY_ENVIRONMENT") == "production"

if is_production:
    # Production: Allow Vercel domains (including preview deployments)
    # Using regex to match all *.vercel.app subdomains for preview deployments
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    # Development: Allow common local development origins
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5500",
        # Local network IP (update if your IP changes)
        "http://192.168.29.66:3000",
        "http://192.168.29.66:5173",
        "http://192.168.29.66:8080",
        # Vercel for testing
        "https://client-wtcfads1b-passionatesandy2004s-projects.vercel.app",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

# 🔴 PUT YOUR REAL LIVEKIT CLOUD VALUES HERE
LIVEKIT_API_KEY = "APIBAAB8kDsU2Za"
LIVEKIT_API_SECRET = "vMZUIaqwcOq3qiUePle2UNGzbcItkIgjtmD16CRXleSB"
LIVEKIT_URL = "wss://community-building-vdqf7nh1.livekit.cloud"

@app.get("/token")
def get_token(room: str, identity: str):
    token = (
        AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)              # ✅ identity goes HERE
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room,
            )
        )
    )

    return {
        "token": token.to_jwt(),
        "url": LIVEKIT_URL,
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
