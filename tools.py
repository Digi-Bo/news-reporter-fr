"""
Ce fichier initialise les outils nécessaires pour les agents, comme la récupération de la clé API pour Serper.
"""

from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API Serper
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# Pour le développement : vérification de la récupération de la clé
# serper_api_key = os.environ['SERPER_API_KEY']
# if not serper_api_key:
#    raise ValueError("La clé API Serper est manquante. Assurez-vous qu'elle est définie dans le fichier .env")
# print(f"Clé API récupérée : {serper_api_key}")

from crewai_tools import SerperDevTool

# Initialiser l'outil pour les capacités de recherche sur internet
tool = SerperDevTool()
