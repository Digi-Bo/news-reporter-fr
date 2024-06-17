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
