# velo-rencontre
A project about meeting new people through being a biking addict 
Un projet permettant de faire de nouvelle rencontre en étant fan de vélo.

Lancement du projet :
`docker-compose up`  


 Le site est accessible via l'url : 
 `localhost`
 
 
5 microservices sont disponibles et mis en place dans notre projet. 
- Map 
- Profile
- Match
- Front
- Authentification

Nous utilisons un token JWT (avec l'algorithme HS256 pour le hashage du mot de passe) pour maintenir les différentes connexions.

Nos API (REST) sont développées en NodeJS, Python (flask).

## Schéma de notre architecture

![alt text][logo]

[logo]: https://i.gyazo.com/3ee10c6c4c4b20475cea4f314f87d0d9.png "Architecture"
