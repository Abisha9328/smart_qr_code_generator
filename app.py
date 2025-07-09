import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
from qr_utils import load_data, save_data, generate_short_code

st.title("🔗 Smart QR Code Generator + Tracker")

data = load_data()

text = st.text_input("Enter URL:")
fg_color = st.color_picker("QR Foreground Color", "#000000")
bg_color = st.color_picker("QR Background Color", "#ffffff")

if st.button("Generate QR Code"):
    if text:
        # Generate unique short code
        short_code = generate_short_code()

        # Save mapping
        data[short_code] = {"original_url": text, "scan_count": 0}
        save_data(data)

        # Create short URL (e.g., http://localhost:8000/r/abc123)
        short_url = f"https://smart-qr-code-generator.onrender.com/r/{short_code}"

        # Generate QR encoding the short URL
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(short_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color, back_color=bg_color)

        # Convert to bytes
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display
        st.image(byte_im, caption="Your QR Code")
        st.write("✅ **Short URL:**", short_url)
        st.download_button("Download QR", byte_im, file_name="qr_code.png")
    else:
        st.warning("Please enter a URL.")
# Display scan count
if st.checkbox("Show Analytics"):
    st.subheader("📊 Scan Analytics")
    if data:
        for code, info in data.items():
            st.write(f"**Short URL:** http://localhost:8000/r/{code}")
            st.write(f"- Original URL: {info['original_url']}")
            st.write(f"- Scan Count: {info['scan_count']}")
            st.markdown("---")
    else:
        st.info("No data yet.")

