from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import shortener
import database

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

@app.post("/shorten")
def shorten_url(item: UrlRequest):
    database.current_id += 1
    unique_id = database.current_id
    short_code = shortener.id_to_short(unique_id)
    database.save_url(item.url, short_code)

    return {"short_url": f"http://127.0.0.1:8000/{short_code}", "code": short_code}

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    # 1. Look up the code in the database
    original_url = database.get_url(short_code)

    if original_url:
        # <--- THIS IS THE MAGIC PART
        # It tells the browser: "Don't show text, just GO to this address!"
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")