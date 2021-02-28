# velo-rencontre
A project about meeting new people through being a biking addict   
Un projet permettant de faire de nouvelles rencontres en étant fan de vélo.

Lancement du projet :
`docker-compose up`  


 Le site est accessible via l'url : 
 `http://localhost`
 
 
5 microservices sont disponibles et mis en place dans notre projet. 
- Map 
- Profile
- Match
- Front
- Authentification

Nous utilison le JSON Web Token (avec l'algorithme HS256 pour le hachage) qui est stocké en localStorage (sur la session du navigateur de l'utilisateur).

Nos API (REST) sont développées en NodeJS, Python (flask), Ajax...

## Schéma de notre architecture

![alt text][logo]

[logo]: https://i.gyazo.com/3ee10c6c4c4b20475cea4f314f87d0d9.png "Architecture"
