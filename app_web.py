import streamlit as st
import qrcode
import qrcode.image.svg
from PIL import Image
from io import BytesIO

# Configuration de la page
st.set_page_config(page_title="Générateur QR Code Pro", page_icon="📱", layout="centered")

st.title("📱 Générateur de QR Code Pro")
st.write("Personnalise la couleur, ajoute un logo et exporte en PNG ou SVG.")

# --- OPTIONS DE SAISIE ---
url = st.text_input("🔗 Entre ton lien ou texte :", placeholder="https://github.com")

col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("🎨 Couleur du QR Code", "#000000")
with col2:
    back_color = st.color_picker("🖼️ Couleur de fond", "#FFFFFF")

# Option Logo
uploaded_logo = st.file_uploader("🖼️ Ajouter un logo au centre (PNG/JPG) :", type=["png", "jpg", "jpeg"])

# Format de sortie
export_format = st.radio("📁 Format d'exportation :", ["PNG", "SVG"], horizontal=True)

# --- GÉNÉRATION ---
if url:
    st.divider()
    
    if export_format == "PNG":
        # Mode PNG
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H if uploaded_logo else qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        # Incrustation du logo
        if uploaded_logo:
            logo = Image.open(uploaded_logo)
            qr_width, qr_height = img.size
            logo_size = int(qr_width * 0.22)
            logo = logo.resize((logo_size, logo_size))
            
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, pos)

        # Préparation du téléchargement
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        st.image(buffer, caption="Aperçu du QR Code PNG", width=280)
        
        st.download_button(
            label="📥 Télécharger le QR Code (PNG)",
            data=buffer,
            file_name="qrcode.png",
            mime="image/png",
            use_container_width=True
        )

    else:
        # Mode SVG (Vectoriel)
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
            image_factory=factory
        )
        qr.add_data(url)
        qr.make(fit=True)

        img_svg = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        buffer_svg = BytesIO()
        img_svg.save(buffer_svg)
        buffer_svg.seek(0)

        if uploaded_logo:
            st.info("ℹ️ L'ajout de logo s'effectue en format PNG pour préserver le rendu vectoriel du SVG.")

        st.success("QR Code SVG vectoriel prêt !")
        
        st.download_button(
            label="📥 Télécharger le QR Code (SVG)",
            data=buffer_svg,
            file_name="qrcode.svg",
            mime="image/svg+xml",
            use_container_width=True
        )
