import streamlit as st
from PIL import Image
import zipfile
import io
import os

st.set_page_config(page_title="Sertifikat + TTD", layout="wide")

st.title("📄 Aplikasi Tempel TTD Sertifikat")

# =========================
# UPLOAD FILE
# =========================
cert_files = st.file_uploader(
    "Upload Sertifikat (bisa banyak)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

sign_file = st.file_uploader(
    "Upload Tanda Tangan (PNG Transparan)",
    type=["png"]
)

# =========================
# POSISI TTD
# =========================
st.sidebar.header("🔧 Pengaturan Posisi")

sign_x = st.sidebar.slider("Posisi X", 0, 2000, 750)
sign_y = st.sidebar.slider("Posisi Y", 0, 4000, 1000)
scale = st.sidebar.slider("Skala TTD (%)", 10, 200, 100)

# =========================
# PREVIEW
# =========================
if cert_files and sign_file:
    signature = Image.open(sign_file).convert("RGBA")

    # resize tanda tangan
    w, h = signature.size
    signature = signature.resize(
        (int(w * scale / 100), int(h * scale / 100))
    )

    st.subheader("👀 Preview Sertifikat")
    sample = cert_files[0]
    cert_img = Image.open(sample).convert("RGBA")

    preview = cert_img.copy()
    preview.paste(signature, (sign_x, sign_y), signature)

    st.image(preview, caption="Preview Sertifikat", use_container_width=True)

    # =========================
    # GENERATE OUTPUT
    # =========================
    if st.button("🚀 Generate Semua Sertifikat"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in cert_files:
                cert = Image.open(file).convert("RGBA")
                cert.paste(signature, (sign_x, sign_y), signature)

                img_bytes = io.BytesIO()
                cert.convert("RGB").save(img_bytes, format="JPEG", quality=95)
                zip_file.writestr(file.name, img_bytes.getvalue())

        zip_buffer.seek(0)

        st.success("✅ Sertifikat berhasil digenerate!")
        st.download_button(
            label="⬇️ Download ZIP",
            data=zip_buffer,
            file_name="sertifikat_output.zip",
            mime="application/zip"
        )

