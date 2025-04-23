
import streamlit as st
import sqlite3
import string
import random
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# Connect or create database
conn = sqlite3.connect("shortener.db", check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute("CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_code TEXT, created_at TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS clicks (id INTEGER PRIMARY KEY AUTOINCREMENT, short_code TEXT, source TEXT, timestamp TEXT)")
conn.commit()

# Generate unique short code
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Store shortened URL
def shorten_url(long_url):
    code = generate_code()
    c.execute("INSERT INTO links (long_url, short_code, created_at) VALUES (?, ?, ?)", (long_url, code, datetime.utcnow().isoformat()))
    conn.commit()
    return code

# QR Code generator
def generate_qr(url):
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    byte_im = buf.getvalue()
    b64 = base64.b64encode(byte_im).decode()
    return f"data:image/png;base64,{b64}"

# UI
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #8360c3, #2ebf91);
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔗 URL Shortener + QR Generator + Tracker")

st.subheader("1. Shorten a URL")
url_input = st.text_input("Enter a long URL")
if st.button("Shorten"):
    if url_input:
        short_code = shorten_url(url_input)
        short_url = f"https://your-domain.onrender.com/{short_code}"
        st.success(f"Short URL: {short_url}")
        st.image(generate_qr(short_url), caption="Scan QR")

st.subheader("2. Tracking Dashboard")
c.execute("SELECT short_code, COUNT(*) FROM clicks GROUP BY short_code")
click_data = c.fetchall()
if click_data:
    st.write("🔍 Clicks by Short Code")
    for code, count in click_data:
        st.write(f"{code} → {count} clicks")

c.execute("SELECT short_code, source, COUNT(*) FROM clicks GROUP BY short_code, source")
by_source = c.fetchall()
if by_source:
    st.write("📊 Clicks by Source")
    for code, src, count in by_source:
        st.write(f"{code} | {src} → {count}")
