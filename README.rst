Apprendre GNU-LINUX
------------------
------------------

C'est un petit logiciel pour apprendre GNU-LINUX avec Python.
Il permet de reviser les commandes de base du systeme.

I. Architecture du systeme
Tout est considere comme fichier sous GNU/LINUX

Quelques emplacements importants pour avoir des infos sur les peripheriques.

/proc
/proc/mounts
/proc/interrupts
/proc/ioports
/proc/dma
/proc/usb
etc...

I.1 Utilitaires pour les peripheriques

-lsmod
Liste tous les modules(pilotes) du noyau

-lscpu
Affiche les infos du processeur
#lscpu -ae
#lscpu --parse

-lsblk
Affiche les infos sur les partitions et les disques du systeme
#lsblk -t
#lsblk -f
#lsblk -f -t
#lsblk -i

-lspci
Affiche les peripheriques connectes sur le slot ou port PCI
#lspci -v
#lspci -m
#lspci -vm ou encore #lspci -vmm
#lspci -t
#lspci -tvm

-lslogins
Affiche les infos sur les utilisateurs du systeme
#lslogins -a (les utilisateurs et la date d'expiration de leur compte)
#lslogins -f (affiche les echecs de connexion des utilisateurs)
#lslogins -L (affiche les infos sur la derniere session de l'utilisateur)

-lsusb
Affiche les infos sur les peripheriques USB
#lsusb
#lsusb -s #bus:#Device (exple: lsusb -s 001:003)
#lsusb -t
#lsusb -v

I.2 Demarrage du systeme(Processus)
        sysvinit
        -------
Les niveaux d'execution du module sysvinit(ancien module gerant le demarrage):
0-->HALT(Arret du systeme)
1-->Single user(un seul utilisateur)
2-->multi-users (plusieurs utilisateurs mais sans chargement du reseau et systeme de fichier distant)
3-->full multi-users(mode complet multi-utilisateurs)
4-->unused(unitilise mais peut etre configure pour d'autres fins)
5-->X11(mode graphique)
6-->reboot(mode redemarrage)

        systemd
        -------
systemd est un système d’initialisation et un daemon qui a été spécifiquement conçu pour le noyau Linux comme alternative à System V. Il a pour but d'offrir un meilleur cadre pour la gestion des dépendances entre services, de permettre le chargement en parallèle des services au démarrage, et de réduire les appels aux scripts shell.

Liste des niveaux d'execution  de systemd
0--> poweroff.target(arret du systeme)
1--> rescue.target(mode mono-utilisateur et mode maintenance)
2--> multi-user.target(pas de chargement du module graphique, mais le reseau est active et multi-utilisateurs)
3--> multi-user.target(pas de chargement du module graphique, mais le reseau est active et multi-utilisateurs)
4--> multi-user.target(pas de chargement du module graphique, mais le reseau est active et multi-utilisateurs)
5--> graphical.target(mode graphique et multi-utilisateurs)
6--> reboot(mode redemarrage)

Repertoire de systemed : /usr/lib/systemd/

