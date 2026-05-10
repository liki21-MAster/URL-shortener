import sqlite3

# 1. Connect to a database file (it will be created automatically)
# check_same_thread=False is needed for FastAPI
connection = sqlite3.connect("urls.db", check_same_thread=False)
cursor = connection.cursor()

# 2. Create the table if it doesn't exist yet
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE
)
""")
connection.commit()

def save_url(original_url: str, short_code: str):
    """Insert the new link into the SQL database."""
    cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (original_url, short_code))
    connection.commit()

def get_url(short_code: str):
    """Search the SQL database for the short code."""
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return the URL string
    return None

def get_next_id():
    """Get the next available ID for our math logic."""
    # We grab the last ID used and add 1
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='urls'")
    result = cursor.fetchone()
    if result:
        return result[0] + 1
    return 1  # Start at 1 if table is empty