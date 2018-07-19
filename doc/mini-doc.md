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

**I.1 Utilitaires pour les peripheriques**

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

Par exemple le dossier /etc/init.d/ contient tous les scripts actifs apres le demarrage de notre systeme Gnu/Linux.
Aussi tous les scripts du dossier /etc/rc3.d/ sont ceux qui s'executent dans le mode 3(multi-utilisateur).
Certains noms de scripts commencent par la lettre S sont ceux de demarrage et les autres avec la lettre K sont les scripts d'arret.

Quelques  majeurs composants de systemd sont:
#systemd: gestionaire des services et du systeme
#systemctl: la commande principale permettant de controler tous les services(activer-arreter-redemarrer-verifier status)
#systemd-analyze: permet d'afficher les performances de votre systeme lors du demarrage.
#networkctl: permet d'afficher les differentes connexion reseaux de votre systeme et leur status(avec option -a)
#journalctl: permet d'afficher le journal des evenements systeme de  systemd

Le dossier /etc/systemd/system/ contient tous les services essentiels et qui ont une priorite tres elevee mais controles par l'administrateur systeme.
Le dossier /usr/lib/systemd/system contient tous les services installes par l'utilisateur

La liste de quelques services et leur extensions
.service --> service system, .swap --> relatif au swap, .socket --> IPC socket(inter-process communication), .timer, etc.

#runlevel
Affiche le niveau d'execution precedent et courant

#systemctl get-default
Affiche la valeur assignee par defaut de notre niveau d'execution

#systemctl set default [nom de votre niveau d'execution]
Assigner la valeur par defaut du niveau d'execution

#systemctl list-units --type=target
Affiche tous les services systeme actifs

#systemctl list-unit-file
Affiche tous les services systemes installes et leur status

#systemctl isolate [niveau execution]
Modifie le niveau d'execution sans changer la valeur assignee par defaut.

Comme la commande #runlevel , init, telinit permettent aussi de changer le niveau d'execution avec sysvinit

#reboot : redemarre le systeme
#shutdown : arrete et redemarre le systeme
        shutdown -h now(arrete maintenant)
        shutdown -r (redemarre)
        shutdown -r #temps (redemarre apres une periode de temps specifie)
        shutdown -c (permet d'annuler le redemarrage)
        shutdown -r 10 -k "Veullez sauvegarder vos fichiers" (va redemarrer la machine dans 10 minutes et envoyer un message a tous les utilisateurs)


