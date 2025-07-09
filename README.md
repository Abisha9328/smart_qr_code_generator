# 🔗 Smart QR Code Generator + Tracker

A simple Streamlit web app to:

✅ Generate QR codes for any URL  
✅ Create unique short URLs (like `http://localhost:8000/r/abc123`)  
✅ Track scan counts for each QR code  
✅ Customize QR code colors  

---

## ✨ Features

- **Smart Short Links:** Automatically generates a unique short code for each URL.
- **QR Code Generation:** Encodes the short URL into a QR image.
- **Color Customization:** Pick your preferred foreground and background colors.
- **Download QR Codes:** Save the generated QR code as a PNG file.
- **Analytics Dashboard:** View all saved URLs and scan counts in one place.

---

## 🚀 How to Run

1. **Install Dependencies**
   ```bash
   pip install streamlit qrcode pillow

(Also ensure you have qr_utils.py with load_data, save_data, and generate_short_code functions.)

Start the App

streamlit run app.py
# Using the App

Enter your URL.

Pick QR colors.

Click Generate QR Code.

Download the QR PNG.

Check Show Analytics to see scan stats.

# 📂 Project Structure

project/
│
├── app.py              # Main Streamlit app
├── qr_utils.py         # Utilities: load_data, save_data, generate_short_code
├── data.json           # (Auto-created) Stores URL mappings and scan counts
└── README.md


# 📈 Tracking Scans
When someone visits a short URL endpoint (e.g., /r/abc123), you should have a separate backend (Flask/FastAPI) to:

Increment scan_count in data.json

Redirect to the original URL

This Streamlit app shows the saved counts.

# ✨ Future Improvements
Add authentication for managing QR codes.

Deploy a backend API to handle redirects.

Add QR expiration dates or limits.

# 📝 License

# DEMO
Live app: https://smartqrcodegenerator-xz2anerh3bbj6zcpkket8w.streamlit.app/


# 💡 Author
ABISHA.S
