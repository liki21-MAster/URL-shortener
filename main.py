import os
import redis
import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()

# 1. Cloud-Native Environment Variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# 2. Prometheus Metrics Exposer
Instrumentator().instrument(app).expose(app)

class URLRequest(BaseModel):
    url: str

@app.post("/shorten")
def shorten_url(req: URLRequest):
    short_id = hashlib.md5(req.url.encode()).hexdigest()[:6]
    cache.set(short_id, req.url)
    return {"short_url": f"http://localhost:8000/{short_id}"}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    long_url = cache.get(short_id)
    if long_url:
        return {"redirect_to": long_url}
    raise HTTPException(status_code=404, detail="URL not found")

# 3. Kubernetes Liveness/Readiness Probe Endpoint
@app.get("/healthz")
def health_check():
    try:
        cache.ping()
        return {"status": "healthy", "database": "connected"}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")