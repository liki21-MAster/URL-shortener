# A simple dictionary to store our data
# Format: { "short_code": "https://original-url.com" }
db = {}

# A counter to act as our Auto-Increment ID
# In a real SQL database, this is handled automatically
current_id = 10000

def save_url(original_url: str, short_code: str):
    """Saves the URL mapping to our fake database."""
    db[short_code] = original_url

def get_url(short_code: str):
    """Retrieves the original URL."""
    return db.get(short_code)