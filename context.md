Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 1/7

Énoncé 

Dans le cadre du projet collaboratif « Superviser et assurer le développement des applications logicielles . », vous 

réaliserez en groupe le cas énoncé ci -dessous « Breizhsport ». 

Le développement de l’application « Breizhsport » est une simulation. 

Étude de cas 

L’entreprise  Breizhsport est une entreprise spécialisée en vente de matériel de sport  qui souhaite se développer sur le 

créneau de la  vente sur internet .

Elle dispose d’un siège à  Rennes , des bureaux à Brest et Lorient,  d’une  usine de fabrication à Brest  et des magasins  dans 

les principales villes de Bretagne. 

La D irection des  Systèmes d’ Information (DSI)  compte 5 0 personnes dont  25 développeurs, 5 chefs de projets, 10 

administrateurs système, 5 SRE  et 5 responsables.  Le système d’information de l’entreprise n’a pas bea ucoup évolué dans 

les dix derniè res années  : les applications sont développé es en PHP /MySQL  avec une méthodologie  de développement 

de cycle en V  et déployées sur des serveurs virtuels dans un fournisseur de hosting français. 

La DSI cherche à moderniser autant le système d’information que  les pratiqu es de développement. P our cela , elle compte 

procéder graduellement en s’appuyant sur le cas pratique du développement d’une application  important e pour le 

dével oppement de l’entreprise  : la nouvelle application de vente par internet. 

Vous arrivez en tant q ue responsable de la nouvelle équipe Modernisati on du Système d’Information. V otre premier 

projet est de définir les nouveau x principes  d’architecture,  de  conception,  de  déploiement et  de  maintenance d es 

applications de Breizhsport. Vous les  valider ez  en  développant  la nouvelle application de vente par internet suivant les 

nouveaux principes. 

La DSI souhaite que cette modernisation du système d’information s’appuie sur quelques piliers  :

1.  Une architecture Cloud Native 

2.  Déploiement  sur  un cloud public . Vous pouvez utiliser un environnement managé local tel que Minikube. 

3.  Environnement de développement industrialisé incluant  :

o Dépôt de code source (SCR) basé sur Git 

o Pipeline de CI/CD 

Pour le reste vous avez un champ d’action assez libre. N’hésitez pas à expérimenter pour que votre POC démontre la 

pertinence des choix effectués (frameworks, patterns et styles architecturaux, communication entre services, résilience, 

scalabilité, qualité du code, systèmes de sécurité, d’audit / monitoring, etc.) 

Vous devez vous appuyer sur le domaine métier (fonctionnel) de l’application de vente en ligne mais l’objectif n’est pas 

de développer l’ensemble des fonctionnalités métiers. L’objectif est de démontrer l’intégration des différentes solutions 

techniques. 

I – Organis er et animer un système de veille active pour actualiser ses compétences sur les méthodes de développement 

et de mise en production 

La direction a constaté que les pratiques  de développement de l’entreprise sont vieillissantes et elle souhaite les 

moderniser en s’appuyant sur un projet phare  : le développement de la nouvelle application de vente sur internet  de 

Breizhsport. Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 2/7

Pour cela, elle a  embauché un nouveau Tech Leader  : vous  serez  à la tête d’une équipe de 5 développeurs avec quelques 

années d’ expérience dans Breizhsport. 

Votre première tâche consistera à mettre en place un système de veille active pour a ctualiser  vos  compétences  ainsi que 

celles  des membres de l’équipe  sur les méthodes de développement et de mise en production .

Vous devez décr ire en détail comment vous allez organiser et ani mer ce système de veille active  et fournir une liste des 

principales sources d’information  sur lesquelles vous allez vous appuyer .

II – Développer des applications complexes en partenariat avec le client ou la MOA en s'adaptant aux différentes 

méthodes de développement et d'hébergement disponibles afin d'apporter la réponse technique la plus juste au client 

La direction vous demande  de proposer une architecture et des méthodes de développement et hébergement modernes 

pour la nouvelle application de vente sur internet, avec quelques piliers  :

1.  Une architecture Cloud Native 

2.  Déploiement sur  un cloud public 

3.  Environnement de développement  industrialisé incluant  :

o Dépôt de code source (SCR) basé sur Git 

o Pipeline de CI/CD 

Elle vous demande d’identifier les architectures et les méthodes les plus adaptées au projet et à l’entreprise , et de bâtir 

des grilles des choix de la méthodologie de déve loppement et d’hébergement de l’application, en incluant le stack 

technologique, le langage et l’environnement de développement. 

III  - Assurer la démonstration de maquettes de solutions technologiques (documentation, schémas,  POC , etc.) auprès 

d'un comman ditaire et expliquer l’adéquation entre les options proposées et le contexte pour conseiller la maîtrise 

d’ouvrage sur les solutions techniques 

Pour valider l’adéquation de ces méthodologies et techniques de développement, la direction vous demande  de fournir 

et  de  commenter un schéma d’architecture et  de  déplo iement pour l’application cible. Vous y inclurez  des notes sur la 

capacité de mise à l’échelle (scalability  en Anglais ), résilience et haute disponibilité, ainsi qu’une justification  des choix 

techniques, de méthodolo gie de développement  et d’hébergement. 

La direction souhaite ensuite avoir  une maquette fonctionnelle ou preuve de concept ( POC ) suivant les principes que vous 

proposez, hébergé dans  un cloud public , afin de pouvoir évaluer la capac ité d’adaptation des principes au monde réel. 

En ce qui concerne la documentation vous pouvez faire le choix d’utiliser un outil «  OpenAPI  » intégré à votre POC. 

IV  - Superviser la mise en place d’une chaine d’intégration continue pour améliorer l’efficie nce des déploiements 

La direction souhaite passer d’un système de test, validation et déploiement manuel à un système d’intégration et 

déploiement continue (CI/CD). Elle vous demande de mettre en place une chaîne CI/CD et de l’appliquer sur la maquette .

La chaîne doit être interfacée au gestionnaire de sources (git), faire passer les tests d’intégration à chaque commit sur la Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 3/7

branche principale et ensuite déployer en production si les tests sont corrects.  Vous pouvez intégrer d’autres types de 

tests dan s votre pipeline, les tests unitaires et d’intégration sont ceux à automatiser à minima. 

V - Se positionner en référent technique auprès de l’équipe de développeurs pour faciliter la résolution de problèmes 

complexes 

On vous demande d’envisager le passage de la  POC  à la production. La direction  souhaite avoir une estimation  des points 

potentiellement problématiques dans le passage de la  POC  à l’application finale (mise à l’échelle, ré silience, haute 

disponibilité…)  ainsi que des pistes de solution. 

VI  - Alimenter la dynamique collective d’apprentissage pour garantir la compétence technique actualisée des 

développeurs et transmettre son savoir 

Pour le passage de la  POC  à l’application finale, l’équipe va devoir gran dir  et inclure des nouveaux développeurs qui ne 

connaissent , ni le projet , ni l’outillage mis en place. Il y aura aussi des développeurs juniors qui vont rejoindre l’équipe. 

Votre travail comme manager d ’équipe sera de mettre en place une démarche d’appren tissage, transmission de 

connaissances et mentorat au sein de l’équipe de développement, avec des actions récurrentes (tech talks, séances de 

partage, pair/mob coding…), pour s’assurer que tous les membres de l’équipe montent en compétence s et que les 

conn aissances sont correctement partagées. 

VII  - Définir la politique qualité logicielle à appliquer à l’ensemble des projets de développement pour assurer l’atteinte 

des objectifs et assainir la dette technique de l’entreprise 

Afin de pouvoir étendre les pri ncipes appliqués dans le projet aux autres projets de l’entreprise, on vous demande de 

poser les bases de la nouvelle politique de qualité logicielle pour un futur  plan d’assurance qualité logiciel (PAQ) .

Le plan doit donner une vision claire et  argumentée des outils et pratiques à mettre en place, en incluant  :

- La culture, autant sur les pratiques de développement (tests, pair/mob programming, revues de code…), que sur 

le fonctionnement de  l’entreprise ( pilotage par la valeur et pas par la date,  démarche agile,  temps dédié à la 

formation …) 

- Les outils  : en plus de s gestionnaires de source et  de la plateforme  CI/CD qui ont déjà été mis en place , des outils 

de qualité du code , des tableaux de bord et des outils de  suivi,  des gestionnaires de projet et des tâches (Jira, 

Asana, Trello…) 

- La gestion de la dette technique 

VII I - Définir la politique de tests à appliquer à l’ensemble des projets de développement afin de garantir le respect du 

périmètre fonctionnel du projet e t la non -régression du SI 

En complément  du plan de qualité logicielle, on vous demande de définir une politique de tests à appliquer dans les 

projets de l’en treprise. Cela doit inclure tous  le s type s de tests  : t est unitaires, tests d’intégration, tests  de  performance ,Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 4/7

tests d’acceptation, tests de non -régression … mais aussi des notions de couverture des tests  (couverture du code, 

couverture fonctionnelle...) , automatisation et mise à disposition des résultats des tests. 

IX - Sécuriser les applications dév eloppées pour garantir l’intégrité du système d’information de l’entreprise et en 

assurer le suivi 

Maintenant , il vous est  demand é de vous pencher sur la sécurité, en deux étapes. 

D’abord, vous devez détailler une proposition de procédure pour garantir la  sécurité de l’application développée par votre 

équipe, avec une description des principaux risques et les actions à mettre en place pour les éviter. 

Ensuite, on vous demande d’éteindre la réflexion avec une proposition de  plan  d’audit systématique de la sécurité du 

système d’information de l’entreprise sur la durée .

X - Définir une démarche d'amélioration continue et garantir le respect des procédures de maintenance applicative 

pour minimiser les ruptures de service et leurs i mpacts sur la production de l’entreprise 

Une fois l’application en production, il faudra gérer son cycle de vie, avec les améliorations, évolutions et maintenances 

que cela comporte. On vous demande  proposer les grandes ligne d’ une démarche d’amélioration  continue pour assurer 

non seulement  un maintien des conditions opérationnelles,  mais  la correction des erreurs, la réduction de la dette 

technique et l’évolutivité de l’application. Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 5/7

Organisation 

Organisation : groupe de 3 à 5 personnes 

La réalisation du sujet est conduite sur la durée du bloc. 

Le jury d’évaluation sera composé du pilote et/ou d’un ou plusieurs intervenants ou professionnels extérieurs. 

Livrables attendus 

Le groupe soutiendra la solution lors d’un oral de 30 minutes comprenant une démonstration du POC suivi d’un échange 

de 10 min avec le jury. 

Le diaporama support devrai présenter le système de veille, les méthodes de développement et les grilles de choix 

technologiques, l’architecture de la solution à développer, le processus CI/CD , les points problématiques pour le 

passage en production, les politiques de qualité logicielle, de tests et de sécurité, la démarche d’amélioration continue 

La soutenance doit inclure les éléments indiquées dans la colonne « Eléments attendus » détaillée ci -après :

Activités évaluées  Compétences évaluées  Eléments attendus 

Maintenir et développer 

son expertise en 

développement 

d’applications 

I – Organiser et animer un système 

de veille active pour actualiser ses 

compétences sur les méthodes de 

développemen t et de mise en 

production 

Description du système de veille mis en place .

Tableau listant les sources de veille identifiées 

II – Développer des applications 

complexes en partenariat avec le 

client ou la MOA en s'adaptant aux 

différentes méthodes de 

développement et d'hébergement 

disponibles afin d'apporter la 

réponse technique la plus juste au 

client 

La description argumentée des méthodes de 

développement les plus adaptés au client 

La justification argumentée du choix 

d’hébergement le plus adapté au client en se 

basant sur des grilles de choix 

La Justif ication argumentées des langages, 

frameworks et autres technologies utilisés en 

se basant sur des grilles de choix 

Code de la maquette fonctionnelle / POC 

Version déployée de la maquette fonctionnelle 

/ POC 

III  - Assurer la démonstration de 

maquettes de solutions 

technologiques (documentation, 

schémas,  POC , etc.) auprès d'un 

commanditaire et expliquer 

Le(s) schéma(s) d’architecture présentant les 

choix effectués 

Intégration d’une d ocumentation basique 

Démonstration du POC démontrant 

l’adéquation avec l’architecture présentée Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 6/7

l’adéquation entre les options 

proposées et le contexte pour 

conseiller la maîtrise d’ouvrage sur 

les solutions techniques 

Démonstration du POC démontrant 

l’intégration des différentes technologies (dont 

CI/CD) proposées 

Manager une équipe de 

développeurs 

IV  - Superviser la  mise en place 

d’une chaine d’intégration 

continue pour améliorer 

l’efficience des déploiements 

Description de la chaîne d’intégration continue 

(CI/CD) proposée 

V - Se positionner en référent 

technique auprès de l’équipe de 

développeurs pour faciliter  la 

résolution de problèmes 

complexes 

Identification des points potentiellement 

problématiques dans le passage de la POC à 

l’application finale, ainsi que des pistes de 

solution. 

VI - Alimenter la dynamique 

collective d’apprentissage pour 

garantir la comp étence technique 

actualisée des développeurs et 

transmettre son savoir 

Description de la démarche d’apprentissage, 

transmission de connaissances et mentorat au 

sein de l’équipe de développement 

Garantir la qualité des 

développements 

VII  - Définir la  politique qualité 

logicielle à appliquer à l’ensemble 

des projets de développement 

pour assurer l’atteinte des 

objectifs et assainir la dette 

technique de l’entreprise 

Description de la politique de qualité logicielle 

VIII  - Définir la politique de tests  à

appliquer à l’ensemble des projets 

de développement afin de garantir 

le respect du périmètre 

fonctionnel du projet et la non -

régression du SI 

Description de la politique de tests 

IX  - Sécuriser les applications 

développées pour garantir 

l’intégrité du  système 

d’information de l’entreprise et en 

assurer le suivi 

Proposition pour garantir la sécurité de 

l’application 

Proposition de systématisation d’un dispositif 

d’audit systématique de la sécurité du système 

d’information de l’entreprise sur la durée Consignes Projet collaboratif 

Consignes projet collaboratif -Superviser et assurer dvpmt - v4.docx 4    

> Consignes projet collaborati f-Superviser et assurer dvpmt -v4.docx 4
> Page 7/7

X - Définir une démarche 

d'amélioration continue et garantir 

le respect des procédures de 

maintenance applicative pour 

minimiser les ruptures de service 

et leurs impacts sur la production 

de l’entreprise 

Description de la démarche d’amélioration 

continue et du plan de maintenance applicative. 

Déroulement 

L’échéancier ci -dessous n’est qu’à titre de conseil. Vous êtes libres de votre organisation. 

Jour  Étapes  Livrables 

J1  -Appropriation du sujet .

-Organisation du groupe .

-Mise en place de la  veille .

Description du  système de veille mis en place 

Tableau listant les sources de veille identifiées 

J2  -Choix des technologies et méthodes de 

développement. 

-schématisation  initiale  de  l’architecture. 

-Démarrage du POC 

Matrices de choix et  justifications des choix techniques et 

méthodologiques 

J3  -Révision de l’architecture 

-Description du processus CI/CD 

-Poursuite du POC dont mise en place du 

CI/CD 

Architecture logicielle 

Pipeline CI/CD 

J4  -Poursuite du POC 

-Réflexion sur le  passage en production 

-définition de la  politique globale de qualité 

logicielle 

-Description de La démarche d’amélioration 

continue 

Points  potentiellement problématiques dans le passage de la 

POC  à l’application finale, ainsi que des pistes de solution. 

Plan d’assurance qualité logicielle 

Plan de maintenance des applications 

J5  -Finalisation du POC 

-Elaboration de la  politique de tests 

-Elaboration de la  démarche de sécurité 

-description de la d émarche 

d’apprentissage et mentorat 

Politique de tests 

Système d’audit de sécurité 

J6  -Finalisation préparation soutenance 

-Soutenance de groupe 

-Retour d’expérience collectif 

Diaporama + POC fonctionnel

- Grille de notation
I – Organiser et animer un système de veille active pour actualiser ses compétences sur les méthodes de développement et de mise en production	
II – Développer des applications complexes en partenariat avec le client ou la MOA en s'adaptant aux différentes méthodes de développement et d'hébergement disponibles afin d'apporter la réponse technique la plus juste au client	
III - Assurer la démonstration de maquettes de solutions technologiques (documentation, schémas, POC , etc.) auprès d'un commanditaire et expliquer l’adéquation entre les options proposées et le contexte pour conseiller la maîtrise d’ouvrage sur les solutions techniques 	
IV - Superviser la mise en place d’une chaine d’intégration continue pour améliorer l’efficience des déploiements	
V - Se positionner en référent technique auprès de l’équipe de développeurs pour faciliter la résolution de problèmes complexes	
VI - Alimenter la dynamique collective d’apprentissage pour garantir la compétence technique actualisée des développeurs et transmettre son savoir	
VII - Définir la politique qualité logicielle à appliquer à l’ensemble des projets de développement pour assurer l’atteinte des objectifs et assainir la dette technique de l’entreprise	
VIII - Définir la politique de tests à appliquer à l’ensemble des projets de développement afin de garantir le respect du périmètre fonctionnel du projet et la non-régression du SI	
IX - Sécuriser les applications développées pour garantir l’intégrité du système d’information de l’entreprise et en assurer le suivi	
X - Définir une démarche d'amélioration continue et garantir le respect des procédures de maintenance applicative pour minimiser les ruptures de service et leurs impacts sur la production de l’entreprise