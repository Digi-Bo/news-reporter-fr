
# Projet d'agents d'IA pour la recherche et l'écriture d'articles avec Gemini


Ce projet utilise le framework Crew AI pour créer des agents d'intelligence artificielle spécialisés dans la recherche et l'écriture de contenus technologiques. L'objectif est de découvrir des technologies révolutionnaires et de produire des articles captivants sur ces découvertes.

## API utilisées
- **Google Gemini** : comme LLM
- **serper.dev** : pour réaliser les recherche sur internet



## Conception d'un projet crewAI

Le projet est structuré autour de plusieurs fichiers principaux :

1. **requirements.txt** : liste des dépendances nécessaires.
2. **agents.py** : définit les agents d'IA pour la recherche et l'écriture.
3. **tasks.py** : décrit les tâches assignées aux agents.
4. **tools.py** : configure les outils utilisés par les agents.
5. **crew.py** : orchestration des agents et des tâches pour exécuter le processus complet.

### Ordre de développement

1. **Configuration des dépendances** : Le fichier `requirements.txt` liste toutes les bibliothèques nécessaires, y compris `crewai`, `langchain_google_genai` pour utiliser les modèles Google Gemini, et `load_dotenv` pour gérer les variables d'environnement.

2. **Définition des agents** : Dans `agents.py`, deux agents sont créés :
    - `news_researcher` : Un agent de recherche senior utilisant le modèle `gemini-1.5-flash` de Google pour découvrir des technologies innovantes.
    - `news_writer` : Un agent d'écriture chargé de rédiger des articles sur les découvertes faites par l'agent de recherche.

3. **Définition des tâches** : Dans `tasks.py`, deux tâches sont définies :
    - `research_task` : Une tâche de recherche visant à identifier les tendances majeures dans un domaine technologique spécifique.
    - `write_task` : Une tâche d'écriture pour composer des articles informatifs et engageants basés sur les résultats de la recherche.

4. **Configuration des outils** : Dans `tools.py`, l'outil `SerperDevTool` est configuré pour fournir des capacités de recherche sur Internet, en utilisant une clé API stockée dans les variables d'environnement.

5. **Orchestration du processus** : Dans `crew.py`, les agents et les tâches sont orchestrés pour former une équipe (`crew`) qui exécute les tâches de manière séquentielle. Le processus est lancé avec un sujet spécifique, et les résultats sont imprimés.

## Documentation du code


### Prérequis

- Assurez-vous d'avoir Python installé sur votre machine. Ce projet utilise `pip` pour la gestion des dépendances.
- Nous vous conseillons d'installer un environnement virtuel avec conda
- Vous devez avoir créé un compte sur serper.dev pour pouvoir utiliser l'API
- Vous devez avoir un compte gmail et créé un compte google cloud pour pouvoir utiliser gemini

### Dépendances

Liste des dépendances requises, définies dans le fichier `requirements.txt` :

```plaintext
crewai
langchain_google_genai #google gemini models
load_dotenv
crewai_tools
langchain_community
tenacity==8.3.0
```

Installez les dépendances en utilisant la commande suivante :

```bash
pip install -r requirements.txt
```

## Configuration

Le projet utilise des variables d'environnement pour gérer les clés API et autres configurations sensibles. Créez un fichier `.env` à la racine du projet et définissez les variables suivantes :

```plaintext
OPENAI_API_KEY=<votre_clé_api_openai>
GOOGLE_API_KEY=<votre_clé_api_google>
SERPER_API_KEY=<votre_clé_api_serper>
```

## Structure du Projet

### Fichiers Principaux

1. `agents.py` : Définit les agents responsables de la recherche et de la rédaction.
2. `tasks.py` : Définit les tâches de recherche et de rédaction.
3. `tools.py` : Initialise les outils nécessaires pour les agents.
4. `crew.py` : Coordonne les agents et les tâches pour exécuter le processus complet.

### Description des Fichiers

#### `agents.py`

```python
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

# Configuration des clés API pour OpenAI et Google
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Appel des modèles Gemini de Google
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
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
```

#### `tasks.py`

```python
"""
Ce fichier définit les tâches à accomplir par les agents de recherche et de rédaction.
"""

from crewai import Task
from tools import tool
from agents import news_researcher, news_writer

# Tâche de recherche
research_task = Task(
    description=(
        "Identifier la prochaine grande tendance dans {topic}. "
        "Se concentrer sur les avantages et les inconvénients et la narrative globale. "
        "Votre rapport final doit clairement articuler les points clés, "
        "les opportunités de marché, et les risques potentiels."
    ),
    expected_output='Un rapport complet de 3 paragraphes sur les dernières tendances de l\'IA.',
    tools=[tool],
    agent=news_researcher,
)

# Tâche de rédaction avec configuration du modèle de langage
write_task = Task(
    description=(
        "Rédiger un article perspicace sur {topic}. "
        "Se concentrer sur les dernières tendances et leur impact sur l'industrie. "
        "Cet article doit être facile à comprendre, engageant, et positif."
    ),
    expected_output='Un article de 4 paragraphes sur les avancées dans {topic}, formaté en markdown.',
    tools=[tool],
    agent=news_writer,
    async_execution=False,
    output_file='new-blog-post.md'  # Exemple de personnalisation de la sortie
)
```

#### `tools.py`

```python
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
```

#### `crew.py`

```python
"""
Ce fichier coordonne les agents et les tâches pour exécuter le processus complet.
"""

from crewai import Crew, Process
from tasks import research_task, write_task
from agents import news_researcher, news_writer

# Formation de l'équipe focalisée sur la technologie avec une configuration améliorée
crew = Crew(
    agents=[news_researcher, news_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

# Démarrage du processus d'exécution des tâches avec un retour amélioré
result = crew.kickoff(inputs={'topic': 'IA dans le secteur de la santé'})
print(result)
```

## Installation et utilisation

1. **Créer un environnement virtuel avec conda**
```
conda create -p venv python==3.12 -y
```
le `p`implique qu'il sera créé dans le dossier de travail


- **Pour l'activer**

```
conda activate ./venv
```

- **Pour le supprimer**
```
rm -rf venv
```



2. **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurez les variables d'environnement :**
    - Créez un fichier `.env` à la racine du projet avec les clés API nécessaires :
      ```
      GOOGLE_API_KEY="votre_cle_api_openai"
      SERPER_API_KEY="votre clé api serper API"
      ```

4. **Lancez le programme :**
    ```bash
    python crew.py
    ```
