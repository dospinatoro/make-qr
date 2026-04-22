import streamlit as st
import segno
from io import BytesIO
from urllib.parse import urlparse
import requests
import threading
import time

# ------------------------
# Helpers
# ------------------------
def keep_alive():
    while True:
        time.sleep(300)  # every 5 minutes
        try:
            requests.get("https://qr-apps.streamlit.app")
        except:
            pass

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except Exception:
        return False

def validationURL(url: str, timeout: int = 5) -> bool:
    if not is_valid_url(url):
        return False
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        if response.status_code >= 400:
            response = requests.get(url, allow_redirects=True, timeout=timeout)
        return response.status_code < 400
    except requests.exceptions.RequestException:
        return False

def generate_qr_buffer(data: str):
    qr = segno.make(data)
    buffer = BytesIO()
    qr.save(buffer, kind="png", scale=5)
    buffer.seek(0)
    return buffer

# ------------------------
# Keeping alive the app
# ------------------------
if "keep_alive_started" not in st.session_state:
    st.session_state.keep_alive_started = True
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="Apps QR Creation", page_icon="🔳")
st.title("QRs for Apps")
st.write("Enter the links in each field, and download each QR individually.")

# ------------------------
# Layout
# ------------------------
col_left, col_center, col_right = st.columns([1, 1, 1])


with col_left:

    google_link = st.text_input("Google Play link")
    ios_link = st.text_input("iOS App Store link")


# QR previews (RIGHT)
with col_center:
    
    for _ in range(5):
            st.empty()

    if google_link and validationURL(google_link):

        google_buffer = generate_qr_buffer(google_link)
        st.download_button(
            label="Download Google QR",
            data=google_buffer,
            file_name="googleApp_qr.png",
            mime="image/png"
        )

        st.image(google_buffer, caption="Google Play Store QR")


with col_right:
    
    for _ in range(7):
            st.empty()

    if ios_link and validationURL(ios_link):

        ios_buffer = generate_qr_buffer(ios_link)
        st.download_button(
            label="Download iOS QR",
            data=ios_buffer,
            file_name="iosApp_qr.png",
            mime="image/png"
        )

        st.image(ios_buffer, caption="iOS App Store QR")



        
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: #888;
    text-align: center;
    font-size: 0.8rem;
}
</style>

<div class="footer">
    © 2026 Daniela Ospina-Toro. Developed for CINC Systems Client Use. Redistribution prohibited.
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
