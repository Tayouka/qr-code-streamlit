import streamlit as st
import qrcode
from io import BytesIO

st.title("📱 Générateur de QR Code")

url = st.text_input("Entre ton lien ou texte :")

if url:
    qr = qrcode.make(url)

    # Convertir l'image en mémoire pour le téléchargement
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Afficher et proposer le téléchargement
    st.image(buffer, caption="Ton QR Code", width=250)
    st.download_button(
        label="📥 Télécharger le QR Code",
        data=buffer,
        file_name="qrcode.png",
        mime="image/png"
    )