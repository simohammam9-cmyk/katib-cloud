# ocr_engine.py - Moteur d'extraction et de parsing des pièces d'identité
import time

def extract_document_data(image_file):
    """
    Extrait les informations d'un document marocain (CNIE, Carte Grise, etc.).
    Simule l'extraction Vision AI / Tesseract et retourne un dictionnaire propre.
    """
    time.sleep(1.2)  # Temps d'inférence Vision AI

    # Données types extraites d'une CNIE marocaine
    extracted_data = {
        "cnie": "BK654321",
        "nom_ar": "محمد العلمي",
        "nom_fr": "Mohamed El Alami",
        "birthdate": "1990-08-15",
        "adresse": "شارع الحسن الثاني، عمارة 12، الدار البيضاء",
        "tel": "0661234567",
        "extra": "12345-أ-6",  # Matricule ou Réf dossier
        "idcs": "1098765432",   # المعرف الرقمي
        "rib": "181330211110000000123456"
    }
    return extracted_data