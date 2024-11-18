# Les 300 meilleurs animes du moment 

## Table des matières 
- [Les 300 meilleurs animes du moment](#les-300-meilleurs-animes-du-moment)
  - [Table des matières](#table-des-matières)
  - [Description générale](#description-générale)
  - [Critères d'évaluation](#critères-dévaluation)
  - [Description du sujet choisi](#description-du-sujet-choisi)
  - [User guide](#user-guide)
    - [Déploiement](#déploiement)
    - [Inscription et connexion](#inscription-et-connexion)
    - [Utilisation de l'application](#utilisation-de-lapplication)
      - [Dashboard Streamlit autour de l'analyse des données](#dashboard-streamlit-autour-de-lanalyse-des-données)
  - [Developer guide](#developer-guide)
    - [Vue d'ensemble](#vue-densemble)
    - [Architecture du code](#architecture-du-code)
      - [Modèles](#modèles)
      - [Schémas](#schémas)
      - [Routes](#routes)
      - [Services](#services)
      - [Templates](#templates)
    - [La base de données](#la-base-de-données)
  - [Les difficultées rencontrées](#les-difficultées-rencontrées)



## Description générale  
Ce projet vise à déployer une application full stack avec FastAPI et PostgreSQL. L'application est conteneurisées via des multi-conteneurs Docker afin de pouvoir lancer aisément l'application sur toute machine. Il existe de nombreux frameworks d'API permettant de développer des applications web performantes et évolutives. Cette unité impose l'utilisation de FastAPI. Ce dernier  est un tout nouveau framework web Python, open source et très performant. Il présente de nombreux avantages comme des méthodes de validation robustes et une documentation automatique et interactive ou encore. De plus, FastAPI propose des mécanismes de sécurité intégrés, comme OAuth2, JWT (JSON Web Tokens), et des permissions de rôle, ce qui le rend bien adapté pour les applications nécessitant une gestion sécurisée des utilisateurs et des ressources. Dans notre application, une authentification sécurisée des utilisateurs est requise, ainsi FastAPI est tout à fait adapté à nos besoins. 


## Critères d'évaluation

Le projet doit se lancer intégralement avec Docker Compose
Le projet doit contenir au moins deux services : 
- Une API écrite en python avec FastAPI
- Une base de données Postgresql
- La base de données contiendra une table User

Un système d'authentification devra être mis en place 
- Soit un simple système comme vu en cours : Récupération d’un JWT à l’aide d’un username / password
- Soit avec le système d’authentification Keycloak
- Au moins un endpoint d’API sécurisé à l’aide d’une authentification JWT

Gestion des erreurs HTTP avec try / except
Utiliser du typing partout 


## Description du sujet choisi

Dans le cadre de notre application, nous avons décidé de nous pencher sur les animes. Plus précisément, nous avons sélectionné les 300 meilleurs animes d'apres [MyAnimeList](https://myanimelist.net/topanime.php). Ce site met à jour quotidiennement le classement des meilleurs animes.    

Ainsi, nous n'avions pas initialement de jeu de données. Nous avons donc créé un jeu de données à partir des informations disponibles sur les 300 premiers animes. Pour ce faire, nous avons scrapé les données du site en utilisant le module Scrapy et en nous basant sur le code source de la page principale et de la page personnalisée de chaque anime. Enfin, nous avons stocké cela dans un fichier csv "anime.csv" qu'on a utilisé par la suite pour insérer nos données dans la base de données Postgres.  

Il y a de nombreuses caractéristiques données sur les animes lorsqu'on inspecte le site. Nous avons sélectionné celles qui nous semblaient le plus intéressantes, dans notre fichier, elles sont nommées de la façon suivante : 
- **rank** : le classement (utilisé comme identifiant dans la base de données)
- **titre** : le titre
- **score** : score obtenu, utilisé pour déterminer le classement
- **episodes** : le nombre d'épisodes, pour les données manquantes (marquées "unknown"), nous avons mis le numéro du dernier épisode sorti
- **statut** : précise si l'anime est en cours ou est terminé
- **studio** : le studio 
- **producteurs** : les producteurs
- **genres_themes** : les genres et thèmes associés à l'anime (sous forme de liste)
- **lien** : le lien pour accéder à la page personnalisée de chaque anime

Notre objectif était donc de concevoir une application permettant à l'utilisateur d'intéragir avec la base de données sur les anime afin qu'il en sache davantage sur les meilleurs animes du moment.  


## User guide

### Déploiement

Premièrement, il vous faut cloner notre projet git, pour cela : 
- Lancez un terminal Bash et aller dans le répértoire qui vous convient pour télécharger le projet
- Copiez cette commande dans le terminal : git clone https://github.com/aumailll/AMAR_AUMAILLE_Full_Stack_Application.git

Pour pouvoir tester et utilisation l'application, il faut disposer de Docker. Si vous ne possédez pas Docker, rendez-vous sur la page de téléchargement officielle de Docker (pour Windows) [ici](https://www.docker.com/products/docker-desktop/). Suivez les instructions d'installation affichées à l'écran ensuite.

Une fois Docker bien installé, vous pouvez réaliser les étapes de lancement de l'application : 
- Dans l'application Docker Desktop, appyez sur "Start Engine" pour démarrer Docker
- Allez dans le répértoire contenant le projet cloné 
- Copiez la commande suivante : docker compose up --build

Il faudra sûrement attendre quelques instants le temps que les conteneurs démarrent et que le téléchargement des données d'anime dans la base de données s'effectue. Voici ce que vous devriez voir dans le terminal une fois que l'application est prête à être utilisée : 
![Terminal Docker](images/terminal_docker.jpg)

Enfin, copiez la ligne suivante dans votre navigateur favori : http://localhost:8000 . Ce lien vous mène à notre application. 


### Inscription et connexion

Si tout s'est bien passé lors du déploiement de l'application, vous arrivez sur une page de connexion / première connexion. 
![Page_connexion](images/connexion.jpg)

Pour accéder au reste de l'application et plus particulièrement pour découvrir des informations sur les animes, la connexion est obligatoire. La première fois il faut renseigner un email et un mot de passe dans le formulaire de "Première connexion", autrement vous recevrez un message d'erreur signifiant que l'email est invalide si vous passez directement par la connexion. Une fois que cette inscription a été réalisée, vous êtes invité à vous connecter en utilisant le formulaire du dessus qui vous redigera directement vers notre page d'accueil. 


### Utilisation de l'application

#### Dashboard Streamlit autour de l'analyse des données



## Developer guide

### Vue d'ensemble

L'application est une plateforme qui interagit avec une base de données PostgreSQL pour gérer des informations sur les animes. Elle est développée avec FastAPI et suit une architecture modulaire organisée autour des concepts de modèles, schemas, services, routers, et de templates HTML pour l'interface utilisateur. Tout cela est contenu dans le dossier "api"

A la racine du projet, il y a ce readme ainsi que le fichier de configuration de Docker Compose, le DockerFile et le dossier "Data" contenant les données sur les animes. Comme nous avons procédé à un scraping des données, il y a également un dossier "anime_fullstack" qui est un projet scrapy, dans les spiders, il y a notamment la spider anime.py. 

### Architecture du code

La majeure partie du travail se situe dans le dossier "api". C'est lui qui contient tous les scripts et la logique liés à FastAPI. 

#### Modèles 
Représentés par le dossier "models" ils contiennent toute la configuration concernant la création des tables, la création de la base de données et l'insertion des données dans les tables. Pour établir un lien avec la base de données, on définit un URL de connexion ainsi que les paramètres d'authentification. On créé aussi un engine et une session, c'est ce qui nous permet d'intéragire avec notre BDD. 

#### Schémas 
Les schémas permettent de conserver l'intégrité des données utilisées par l'application. Ils utilisent Pydantic pour valider les données reçues ou envoyées via l'API et s'assurent que les données échangées entre le front et le end respectent le format attendu. Nous avons défini des schémas pour les données des users, des animes et du token généré. 

#### Routes
Les routes permettent de découper les points d'accès de l'API en modules logiques. Elles se trouvent dans le dossier "routers" de notre projet. Elles définissent l'interface de communication et l'interface d'interaction avec l'application. Elles suivent la logique CRUD: create, read, update, delete.

#### Services
Ils contiennent la logique métier et les interactions complexes avec la base de données.Ils permettent d'effectuer des traitements de données (par exemple sélectionner les 10 premiers éléments). 

#### Templates
Il s'agit de la partie frontend. Ce sont des pages html pour accueillir les utilisateurs. Ils permettent de rendre dynamiquement des pages web avec Jinja2.  

<div style="text-align: center;">
    <img src="images/fastapi.jpg" alt="Fast API" width="600"/>
</div>

### La base de données 

PostgreSQL, souvent connu sous le nom de postgres est un système de gestion de bases de données relationnelles open-source. Il est conçu pour gérer de grandes quantités de données tout en offrant des performances élevées. Comme il s'agit d'un système de base de données relationnelles, il repose sur la notion de "tables" et des règles strictes concernant les attributs de ces tables. Dans le cadre de notre application, nous utilisons postgres pour définir et remplir les tables Anime et User qui contiennent respectivement les informations sur les meilleurs animes et les informations de connexion des utilisateurs. Par ailleurs, postgres permet également le stockage des données non relationnelles type JSON. C'est donc un outil très intéressant.  
Comme nous l'avions mentionné plus haut, nous utilisons l'image officielle proposée par Docker avec la dernière version (spécifiée dans le docker compose) de postgres pour l'utiliser. 


## Les difficultées rencontrées 
Au cours du développement de notre application, nous avons rencontré quelques difficultés. Nous avons découvert le framework FastAPI et le système de base de données Postgres. De plus, l'année dernière, nous n'avions pas fait un dashboard avec Flask, nous n'avions donc pas cette premiere expérience avec les APIs.  
La première difficultée abordée a été l'insertion des données : à l'origine, nous voulions directement intégrer dans la table dédiée aux animes les animes scrapés. L'objectif était donc de lancer le scraping et automatiquement insérer les données dans la table "anime". Nous avons perdu beaucoup de temps dessus en raison de petits détails (données manquantes, problèmes de caractères spéciaux, données numériques considérées comme textuelles...) Ainsi, nous avons choisi de stocker les données en local, de nettoyer le csv obtenu pour avoir le format attendu pour la table dans la base de données et enfin de stocker les valeurs. 
Nous nous sommes aussi "fait avoir" avec les volumes persistants, ce qui a entraîné une grande perte de temps à essayer de résoudre des corrections déjà apportées alors qu'il nous suffisait de supprimer les volumes persistants (docker volume rm nom_volume). 



