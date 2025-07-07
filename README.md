## Initialisation du projet Rasa
Lancement via docker
```
docker-compose up --build
```

Lancer le webhook dans un container
```
docker-compose -it exec alma_chatbot bash
rasa run actions
```

Lancer l'entrainement et l'execution du bot dans un autre container
```
docker-compose -it exec alma_chatbot bash
rasa train --force
rasa shell
```

Utiliser la commande `exit` dans le conteneur pour en sortir et la commande `docker-compose down` pour arrêter le conteneur

## Commande implémenter
- Saluer l'utilisateur
- Commander une pizza
- Demander le menu
- Demander l'horaires d'ouverture
- Demander le prix d'une pizza
- Remercier une information donnée
- Dire au revoir

