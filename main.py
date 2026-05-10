import string
import random
import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

# 1. Initialize FastAPI app
app = FastAPI(title="DevOps URL Shortener API")

# 2. Connect to Redis (Docker Compose automatically routes 'redis' to the DB container)
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# 3. Enable Prometheus Metrics for monitoring
Instrumentator().instrument(app).expose(app)

# 4. Define the data structure for POST requests
class URLRequest(BaseModel):
    long_url: str

# Helper function to generate a random 6-character string
def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# ==========================================
# SPECIFIC ROUTES (These must ALWAYS go first)
# ==========================================

@app.get("/healthz")
def health_check():
    try:
        # Ping the database to prove it is alive
        redis_client.ping()
        return {"status": "healthy", "database": "connected"}
    except redis.ConnectionError:
        # If Redis is dead, fail the health check
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.post("/shorten")
def create_short_url(request: URLRequest):
    short_id = generate_short_id()
    
    # Save the mapping in Redis: { "abc123": "https://google.com" }
    redis_client.set(short_id, request.long_url)
    
    return {
        "short_id": short_id, 
        "long_url": request.long_url,
        "message": "URL successfully shortened!"
    }


# ==========================================
# CATCH-ALL ROUTES (These must ALWAYS go last)
# ==========================================

@app.get("/{short_id}")
def redirect_to_url(short_id: str):
    # Ask Redis if it has a long URL saved for this short ID
    long_url = redis_client.get(short_id)
    
    if long_url:
        # If found, instantly redirect the user
        return RedirectResponse(url=long_url)
    else:
        # If not found, throw your custom 404 error
        raise HTTPException(status_code=404, detail="URL not found")