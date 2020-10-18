# **Service.py**

Une simple fenêtre Tkinter, à l'apparence d'un panneau de contrôle, offrant un raccourci directe aux services web linux installer sur la machine, à la fois compatible avec python2 et python3.

---

## **Aperçu**

![ihm.png](screenshots/ihm.png)

---

## **Mode de lancement**

- Lancement normal avec les commandes des services Apache2 et MySQL
```
:~$ python service.py
```

- Lancement en mode Tor ajoutant les commandes du service Tor si il est installer
```
:~$ python service.py -t
:~$ python service.py --tor
```

---

## **Arguments**

### Syntax pour afficher la liste des arguments

```
:~$ python service -h
:~$ python service -?
:~$ python service --help
```

### Liste des arguments

| Option     | Option longue GNU | Description                          |
| ---------- | ----------------- | ------------------------------------ |
| `-a`       | `--about`         | A propos du soft                     |
| `-c`       | `--check`         | Vérifie l'existance des services Web |
| `-h`, `-?` | `--help`          | Affiche ce message                   |
| `-l`       | `--list`          | Liste tous le repertoire du serveur  |
| `-t`       | `--tor`           | Lancement en mod Tor                 |
| `-v`       | `--version`       | Affiche la version du soft           |

---

## **Gestion des Ressources & Configurations**

Dès le démarrage de l'app, une analyse rapide des services présents sur la machine s'éxecute afin de voir si les services Apache2, MySQL et Tor sont bien installé, l'app ne démarrera qu'une fois les 3 services détecter sur la machine.

Un accès direct au fichier de configuration du service avec le bouton "CONFIG", une fois le panneau d'édition ouvert, vous pouvez modifier les paramètres dès que vous avez terminer l'édition.

![conf.png](screenshots/conf.png)

L'accès direct au fichier log d'erreur et d'accès au serveur apache est aussi accessible dans le menu contextuel de l'app.

![log.png](screenshots/log.png)

Si jamais vous auriez besoin de faire plus que l'app vous propose, vous pouvez accéder au shell depuis l'app en cliquant sur le bouton "Terminal", une console s'ouvrira en mode admin.

---

## **Pré-requis**

- Installation de Python 2 ou 3
- Installation du module "Tkinter" pour python2 ou "tkinter" pour python3
- Lancement en mode administrateur (Demande un mot de passe lors du lancement de l'app dans le shell)
- Compatible uniquement sous Linux

---

## **Téléchargement**

- **[Service.zip](https://github.com/Tracks12/service.py/releases/download/0.0.7-a/Service.zip)**
- [Code Source zip](https://github.com/Tracks12/service.py/archive/0.0.7-a.zip)
- [Code Source tar.gz](https://github.com/Tracks12/service.py/archive/0.0.7-a.tar.gz)

---

## **License**

Code sous license [GNU License](https://www.gnu.org/licenses/gpl-3.0.html)
