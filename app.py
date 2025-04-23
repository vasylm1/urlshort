import streamlit as st
from database import init_db, add_url, get_url, get_analytics
from utils import generate_short_code, generate_qr_code, is_valid_url
import base64
from datetime import datetime

# Initialize database
init_db()

# Custom CSS for gradients
st.markdown("""
    <style>
    .gradient-text {
        background: linear-gradient(45deg, #6e48aa, #9d50bb);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 3em !important;
        font-weight: bold !important;
    }
    .gradient-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# App layout
st.markdown('<p class="gradient-text">URL Shorty</p>', unsafe_allow_html=True)
st.caption("Shorten, track, and analyze your links")

# Main functionality
tab1, tab2, tab3 = st.tabs(["🔗 Shorten URL", "📊 Analytics", "⚙️ Redirect Logic"])

with tab1:
    with st.container():
        st.markdown('<div class="gradient-box">', unsafe_allow_html=True)
        
        url = st.text_input("Enter your long URL", placeholder="https://example.com/very-long-url")
        
        col1, col2 = st.columns(2)
        with col1:
            custom_code = st.text_input("Custom short code (optional)", placeholder="my-link")
        with col2:
            st.write("")  # Spacer
            generate_btn = st.button("Generate Short URL")
        
        if generate_btn and url:
            if not is_valid_url(url):
                st.error("Please enter a valid URL (include http:// or https://)")
            else:
                short_code = custom_code if custom_code else generate_short_code()
                try:
                    add_url(url, short_code)
                    short_url = f"https://your-domain.com/{short_code}"  # Change this in production
                    
                    st.success("URL shortened successfully!")
                    st.code(short_url, language="markdown")
                    
                    # Generate QR code
                    qr_img = generate_qr_code(short_url)
                    st.image(qr_img, caption="Scan this QR code", width=200)
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download QR Code",
                            data=qr_img,
                            file_name=f"qr_{short_code}.png",
                            mime="image/png"
                        )
                    with col2:
                        st.write("")  # Spacer
                except sqlite3.IntegrityError:
                    st.error("This custom code is already taken. Please try another one.")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Link Analytics")
    short_code = st.text_input("Enter short code to view analytics", placeholder="abc123")
    
    if short_code:
        analytics = get_analytics(short_code)
        if analytics["original_url"]:
            st.subheader(f"Analytics for: {analytics['original_url']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Clicks", analytics["total_clicks"])
                st.write(f"Created on: {analytics['created_at']}")
            with col2:
                st.write("**Traffic Sources**")
                for source, count in analytics["referrers"].items():
                    st.write(f"- {source}: {count}")
            
            # Simple chart
            if analytics["referrers"]:
                st.bar_chart({"Clicks": analytics["referrers"]})
        else:
            st.warning("No analytics found for this short code")

with tab3:
    st.header("Redirect Logic (For Production)")
    st.write("""
    For production, you'll need to:
    1. Deploy this with FastAPI/Flask to handle redirects
    2. Set up a custom domain
    3. Add redirect logic like:
    """)
    
    st.code("""
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import RedirectResponse
    
    app = FastAPI()
    
    @app.get("/{short_code}")
    async def redirect_url(short_code: str, referrer: str = "direct"):
        original_url = get_url(short_code)
        if original_url:
            record_click(short_code, referrer)
            return RedirectResponse(url=original_url)
        raise HTTPException(status_code=404)
    """, language="python")

# Footer
st.markdown("---")
st.caption("Built with Streamlit | [GitHub Repo](#)")
