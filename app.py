import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Définition des fonctions
def adjust_contrast_brightness(image, alpha=1.2, beta=30):
    """
    Ajuste le contraste et la luminosité d'une image.
    alpha : facteur de contraste (1.0 = normal, >1 = plus de contraste)
    beta : facteur de luminosité (0 = normal, >0 = plus lumineux)
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def apply_gaussian_blur(image, ksize=5):
    """
    Applique un flou gaussien pour réduire le bruit.
    ksize : taille du noyau de flou (doit être un nombre impair)
    """
    blurred = cv2.GaussianBlur(image, (ksize, ksize), 0)
    return blurred

def apply_threshold(image, threshold_value=128):
    """
    Applique un seuillage binaire pour isoler les zones claires et sombres.
    threshold_value : valeur seuil (0-255)
    """
    _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded

# Titre de l'application
st.title("Application de Conversion d'Images Médicales en Niveaux de Gris")

# Upload d'une image
uploaded_file = st.file_uploader("Choisissez une image scanner", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Charger l'image avec PIL
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # Convertir en tableau numpy

    # Vérifier si l'image est bien chargée
    if image_np is not None:
        # Afficher l'image originale
        st.image(image, caption="Image Originale", use_container_width=True)

        # Conversion en niveaux de gris avec OpenCV
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        st.image(image_gray, caption="Image en Niveaux de Gris", use_container_width=True, channels="GRAY") # Afficher l'image convertie

        # Réglage du contraste et de la luminosité
        alpha = st.slider("Contraste", 0.5, 3.0, 1.2)  # Ajuster le contraste
        beta = st.slider("Luminosité", -100, 100, 30)  # Ajuster la luminosité
        image_adjusted = adjust_contrast_brightness(image_gray, alpha, beta)
        st.image(image_adjusted, caption="Contraste & Luminosité Ajustés", use_column_width=True) # Afficher l'image convertie

        # Appliquer un flou
        ksize = st.slider("Flou (Taille du noyau)", 1, 15, 5, step=2)  # Doit être impair
        image_blurred = apply_gaussian_blur(image_adjusted, ksize)
        st.image(image_blurred, caption="Image avec Flou Gaussien", use_column_width=True) # Afficher l'image convertie

        # Appliquer un seuillage
        threshold_value = st.slider("Valeur du Seuillage", 0, 255, 128)
        image_thresholded = apply_threshold(image_blurred, threshold_value)
        st.image(image_thresholded, caption="Image Seuillée (Binaire)", use_column_width=True) # Afficher l'image convertie        

        # Ajouter une option de téléchargement de l'image convertie
        _, buffer = cv2.imencode(".jpg", image_gray)
        st.download_button("Télécharger l'image traitée", buffer.tobytes(), file_name="image_processed.jpg", mime="image/jpeg")
