Lien du discord :

https://discord.gg/AuvvU7f4QX

Liens github :

https://github.com/El-lulu/Bot-discord-Collectron.git


GUIDE DES COMMANDES 


/coins
Affiche le montant de Coins que le joeur possède.

/work
Vous permet de travailler pour gagner un salaire aléatoire (entre 10 et 50 Coins).
Restriction : Utilisable une fois par heure.

/leaderboard
Affiche le classement (Top 10) des membres les plus riches du serveur.


Commandes qui gère la boutique et les objets

/boutique
Ouvre le catalogue interactif des objets en vente. Utilisez les boutons pour changer de page.

/inspect [nom_objet]
Affiche la fiche technique d'un objet (Prix d'achat, Prix de revente, Stock restant) et affiche l'image de l'objet.

/buy [nom_objet]
Achète l'objet spécifié. Le coût est immédiatement retiré de votre solde.

/inventory
Affiche le contenu de votre sac à dos (la liste de tous vos objets).

/sell [nom_objet]
Vend un objet de votre inventaire à la boutique pour récupérer des Coins.


Commandes de jeux et de paris

/slots [mise]
Lance la machine à sous.
Gains possibles :
- 3 Sept (7) : Jackpot (x10)
- 3 Diamants : x5
- 3 Fruits identiques : x3
- 2 Symboles identiques : x1.5

/pfc [choix] [mise]
Joue à Pierre-Feuille-Ciseaux contre le Bot.
Règle : C'est du "Quitte ou Double". Si vous gagnez, vous doublez votre mise. Si vous perdez, vous perdez votre mise.


COMMANDES ADMIN 

Attention si tu n'a pas les perm tu ne verra pas afficher ses commandes

/admin help
Affiche la liste des commandes d'administration (visible seulement par vous).

/admin create_item [nom] [prix] [vente] [emoji] [stock] [image]
Crée un nouvel objet disponible dans la boutique.
Note : Le paramètre [image] doit correspondre au nom exact du fichier dans le dossier images (ex: epee.png).

/admin set_stock [nom_objet] [quantité]
Change manuellement la quantité disponible d'un objet.

/admin give_coins [membre] [montant]
Crée de l'argent et le donne au membre spécifié.

/admin remove_coins [membre] [montant]
Retire de l'argent du compte d'un membre.