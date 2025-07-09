import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import requests
import random
import string

st.title("🔗 Smart QR Code Generator + Tracker")

# Input fields
text = st.text_input("Enter URL:")
fg_color = st.color_picker("QR Foreground Color", "#000000")
bg_color = st.color_picker("QR Background Color", "#ffffff")

if st.button("Generate QR Code"):
    if text:
        # Generate unique short code
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Create short URL for QR code
        short_url = f"https://smart-qr-backend.onrender.com/r/{short_code}"

        # Save mapping via FastAPI backend
        api_url = "https://smart-qr-backend.onrender.com/api/create"
        payload = {"short_code": short_code, "original_url": text}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            st.success("Short URL created successfully!")
        else:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except Exception:
                error_detail = response.text
            st.error("Error creating short URL: " + error_detail)

        # Generate QR encoding the short URL
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(short_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color, back_color=bg_color)

        # Convert to bytes
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display QR code and download link
        st.image(byte_im, caption="Your QR Code")
        st.write("✅ **Short URL:**", short_url)
        st.download_button("Download QR", byte_im, file_name="qr_code.png")
    else:
        st.warning("Please enter a URL.")

# Analytics section (optional, requires backend API)
if st.checkbox("Show Analytics"):
    st.subheader("📊 Scan Analytics")

    try:
        analytics_url = "https://smart-qr-backend.onrender.com/api/data"
        response = requests.get(analytics_url)

        if response.status_code == 200:
            data = response.json()
            if data:
                for code, info in data.items():
                    st.write(f"**Short URL:** https://smart-qr-backend.onrender.com/r/{code}")
                    st.write(f"- Original URL: {info['original_url']}")
                    st.write(f"- Scan Count: {info['scan_count']}")
                    st.markdown("---")
            else:
                st.info("No data yet.")
        else:
            st.error("Could not fetch analytics data.")
    except Exception as e:
        st.error(f"Error fetching analytics: {e}")
