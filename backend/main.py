from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas
from app.api import auth, policy, events
import os

# Create tables (for MVP simplicity, usually use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NIRA-X-Guardian API")

# CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5354,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        demo_email = "user@db"
        demo_password = "password"
        user = db.query(models.User).filter(models.User.email == demo_email).first()
        if not user:
            from app.api.auth import get_password_hash
            hashed_password = get_password_hash(demo_password)
            new_user = models.User(email=demo_email, hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            print(f"Created demo user: {demo_email}")
    except Exception as e:
        print(f"Error seeding demo user: {e}")
    finally:
        db.close()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(policy.router, prefix="/api/policy", tags=["policy"])
app.include_router(events.router, prefix="/api/events", tags=["events"])

@app.get("/")
def read_root():
    return {"message": "NIRA-X-Guardian API is running"}

@app.get("/blockpage/{family_id}", response_class=HTMLResponse)
def get_block_page(family_id: int):
    # Simple template for block page
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Site Blocked - NIRA-X-Guardian</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ text-align: center; background: white; padding: 3rem; border-radius: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 500px; }}
            .x-icon {{ font-size: 8rem; color: #ef4444; margin-bottom: 1rem; animation: pulse 2s infinite; }}
            h1 {{ color: #1f2937; margin-bottom: 0.5rem; }}
            p {{ color: #6b7280; margin-bottom: 2rem; }}
            .btn {{ background-color: #3b82f6; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; transition: background-color 0.2s; border: none; cursor: pointer; }}
            .btn:hover {{ background-color: #2563eb; }}
            @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="x-icon">X</div>
            <h1>Access Blocked</h1>
            <p>This website has been blocked by your family's safety policy.</p>
            <button class="btn" onclick="requestOverride()">Request Override</button>
        </div>
        <script>
            function requestOverride() {{
                const domain = new URLSearchParams(window.location.search).get('domain');
                if (!domain) {{ alert('No domain specified'); return; }}
                fetch('/api/policy/override/request', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ domain: domain, family_id: {family_id} }})
                }})
                .then(res => res.json())
                .then(data => alert('Override requested! Token: ' + data.token))
                .catch(err => alert('Error requesting override'));
            }}
        </script>
    </body>
    </html>
    """
