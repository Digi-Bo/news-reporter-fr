"""
Ce fichier définit les agents responsables de la recherche et de la rédaction.
"""

from crewai import Agent
from tools import tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Charger les variables d'environnement
load_dotenv()


# Appel des modèles Gemini de Google
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Création d'un agent de recherche senior avec mémoire et mode verbeux
news_researcher = Agent(
    role="Chercheur Senior",
    goal='Découvrir des technologies révolutionnaires dans {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Poussé par la curiosité, vous êtes à la pointe de"
        "l'innovation, désireux d'explorer et de partager des connaissances"
        "qui pourraient changer le monde."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

# Création d'un agent rédacteur avec des outils personnalisés pour rédiger des articles
news_writer = Agent(
    role='Rédacteur',
    goal='Raconter des histoires technologiques captivantes sur {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Avec un talent pour simplifier les sujets complexes, vous créez"
        "des narrations engageantes qui captivent et éduquent, mettant en lumière"
        "les nouvelles découvertes de manière accessible."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=False
)
