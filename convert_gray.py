import cv2

# Charger l'image en couleur
image_color = cv2.imread("scanner_image.jpg")

# Vérifier que l'image est bien chargée
if image_color is None:
    print("❌ Erreur : l'image n'a pas été trouvée ! Vérifiez son emplacement.")
else:
    # Conversion en niveaux de gris
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

    # Sauvegarder l'image convertie
    cv2.imwrite("scanner_image_gray.jpg", image_gray)

    print("✅ Conversion terminée ! L'image en niveaux de gris est enregistrée sous 'scanner_image_gray.jpg'.")
