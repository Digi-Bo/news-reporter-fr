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
        "Rédiger en français un article pertinent sur {topic}. "
        "Se concentrer sur les dernières tendances et leur impact sur l'industrie. "
        "Cet article doit être facile à comprendre, engageant, et positif."
        "Fait bien attention à respecter les règles typographiques concernant les majuscules dans les titres."
        
    ),
    expected_output='Un article de 4 paragraphes sur les avancées dans {topic}, formaté en markdown.',
    tools=[tool],
    agent=news_writer,
    async_execution=False,
    output_file='new-blog-post.md'  # Exemple de personnalisation de la sortie
)
