import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('url_shorty.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT NOT NULL,
                  short_code TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  clicks INTEGER DEFAULT 0)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS clicks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  url_id INTEGER,
                  referrer TEXT,
                  clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(url_id) REFERENCES urls(id))''')
    
    conn.commit()
    conn.close()

def add_url(original_url, short_code):
    conn = sqlite3.connect('url_shorty.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
              (original_url, short_code))
    conn.commit()
    conn.close()

def get_url(short_code):
    conn = sqlite3.connect('url_shorty.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def record_click(short_code, referrer="direct"):
    conn = sqlite3.connect('url_shorty.db')
    c = conn.cursor()
    
    # Update click count
    c.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code=?", (short_code,))
    
    # Record click details
    c.execute("SELECT id FROM urls WHERE short_code=?", (short_code,))
    url_id = c.fetchone()[0]
    c.execute("INSERT INTO clicks (url_id, referrer) VALUES (?, ?)", (url_id, referrer))
    
    conn.commit()
    conn.close()

def get_analytics(short_code):
    conn = sqlite3.connect('url_shorty.db')
    c = conn.cursor()
    
    # Get basic info
    c.execute("SELECT original_url, created_at, clicks FROM urls WHERE short_code=?", (short_code,))
    url_info = c.fetchone()
    
    # Get referrer breakdown
    c.execute('''SELECT referrer, COUNT(*) as count 
                 FROM clicks 
                 JOIN urls ON clicks.url_id = urls.id 
                 WHERE urls.short_code=? 
                 GROUP BY referrer''', (short_code,))
    referrers = c.fetchall()
    
    conn.close()
    
    return {
        "original_url": url_info[0],
        "created_at": url_info[1],
        "total_clicks": url_info[2],
        "referrers": dict(referrers)
    }
