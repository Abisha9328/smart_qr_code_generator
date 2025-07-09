import streamlit as st
import qrcode
from io import BytesIO

st.title("🔗 Simple QR Code Generator")

text = st.text_input("Enter the URL to encode:")
fg_color = st.color_picker("QR Foreground Color", "#000000")
bg_color = st.color_picker("QR Background Color", "#ffffff")

if st.button("Generate QR Code"):
    if text:
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color, back_color=bg_color)

        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(byte_im, caption="Your QR Code")
        st.download_button("Download QR", byte_im, file_name="qr_code.png")
    else:
        st.warning("Please enter a URL.")
