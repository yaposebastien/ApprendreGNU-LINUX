Apprendre les commandes de base de GNU/LINUX avec Python3
--------------------------------------------------------
--------------------------------------------------------



Table des matières
------------------


1. 101: Architecture du système
2. 102: Installation Linux et gestion des paquets
3. 103: Commandes GNU et Unix
4. 104: Périphériques, systèmes de fichiers Linux, norme de hiérarchie du système de fichiers



        1. 101: Architecture du système

Tout est considere comme fichier sous GNU/LINUX.
Quelques emplacements importants pour avoir des infos sur les peripheriques.

*/proc
*/proc/mounts
*/proc/interrupts
*/proc/ioports
*/proc/dma
*/proc/usb


                1. 101.1 Utilitaires pour les peripheriques**

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
Scenario 1: Afficher la liste de partition et retrouver les infos du systeme de fichier sur un specifiquement
$lsblk
$lsblk --nodeps -f /dev/sda11

-lspci
Affiche les peripheriques connectes sur le slot ou port PCI
#lspci -v
#lspci -m
#lspci -vm ou encore #lspci -vmm (offre ses infos avec plus de details)
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

101.2 Demarrage du systeme(Processus)
        sysvinit
        C'est un package contenant u group de processus qui est responsable du control basic des fonctions du systeme. Il inclut "init" qui est la premiere application a s'executer du noyau. Init controle le demarrage, running et arret de tous les programmes.
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

Liste des niveaux d'execution  de systemd ou target
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

101.3 Change Runlevels/Boot Targets and Shutdown or Reboot the System.

Quelques  majeurs composants de systemd sont:
#systemd: gestionaire des services et du systeme
#systemctl: la commande principale permettant de controler tous les services(activer-arreter-redemarrer-verifier status)
#systemd-analyze: permet d'afficher les performances de votre systeme lors du demarrage.
#networkctl: permet d'afficher les differentes connexion reseaux de votre systeme et leur status(avec option -a)
#journalctl: permet d'afficher le journal des evenements systeme de  systemd

Le dossier /etc/systemd/system/ contient tous les services essentiels et qui ont une priorite tres elevee mais controles par l'administrateur systeme.
Le dossier /run/systemd/system contient tous les services installes lorsque la machine a deja demarree
Le dossier /usr/lib/systemd/system contient tous les services installes par l'utilisateur

La liste de quelques services et leur extensions
.service --> service system, .swap --> relatif au swap, .socket --> IPC socket(inter-process communication), .timer, etc.

#runlevel
Affiche le niveau d'execution precedent et courant

#telint number
Modifie le niveau d'execution de la machine exple: #telinit 0 (arret de la machine)

#systemctl get-default
Affiche la valeur assignee par defaut de notre niveau d'execution

#systemctl cat graphical.target
Affiche les details du target graphical.target

#systemctl list-unit-files -t target
Affiche tous la liste des services disponibles

#systemctl set default [nom de votre niveau d'execution]
Assigner la valeur par defaut du niveau d'execution exple: #systemctl set-default multi-user.target

#systemctl list-units --type=target
Affiche tous les services systeme actifs

#systemctl list-unit-files
Affiche tous les services systemes installes et leur status

#systemctl isolate [niveau execution]
Modifie le niveau d'execution sans changer la valeur assignee par defaut.
Comme la commande #runlevel , init, telinit permettent aussi de changer le niveau d'execution avec sysvinit

#systemctl rescue
Modifie notre niveau d'excecution courant pour le rescue mode

#Systemctl reboot
Permet de redemarrer la machine


#reboot : redemarre le systeme
#shutdown : arrete et redemarre le systeme
        shutdown -h now(arrete maintenant)
        shutdown -r (redemarre)
        shutdown -r #temps (redemarre apres une periode de temps specifie)
        shutdown -c (permet d'annuler le redemarrage)
        shutdown -r 10 -k "Veullez sauvegarder vos fichiers" (va redemarrer la machine dans 10 minutes et envoyer un message a tous les utilisateurs)
        shutdown -h 1 minute(Permet de redemarrer la machine dans une minute)
#wall
Permet de diffuser un message aux utilisateurs connectes a la machine

Topic 102: Linux Installation and Package Management
102.1 Conception du schéma de partitionnement
Liste partielle de termes, fichiers et utilitaires utilisés pour cet objectif :

    système de fichiers racine /
    système de fichiers /var (les fichiers log, fichiers de donnees binaires, fichiers et repertoires partages)
    système de fichiers /home
    système de fichiers /boot
    espace d'échange swap
    système de fichiers /opt (en general pour heberges les dossiers des applications tierces comme skypeforlinux, eclipse, google, etc)

#mount
Permet de monter des partitions mais aussi d'afficher toutes les partitions

#lsblk
Affiche toutes les partitions et leur noms

#fdisk -l [nom partition]
Affiche toutes les infos d'une partition specifique exple: #fdisk -l /dev/sda

#swapon --summary
Affiche les details de notre partition swap active

!Logical Volume
Connaitre ses avantages
 -Flexible(augmentation et reduction de la taille)
 -Snaphots(image du volume a un instant donne essentiel pour la sauvegarde, restauration sans endommager le volume)
 #pvs
 Affiche toute la liste des volumes

 #vgs
Affiche tous les groupes de volumes logiques

#lvs
Affiche tous les volumes logiques

102.2 Installation d'un gestionnaire d'amorçage

GRUB(Legacy)
Son dossier est /boot/grub/grub.cfg (Centos base os)

GRUB2
Quelques examples de commandes de configuration de grub2

Pour Red Hat => grub2-<command>
Pour Debian => grub-<command>

#grub2-editenv list
Affiche la liste des entrees pour le fichier de configuration de GRUB

!Pour consulter le details de configuration de Grub est le fichier #/etc/default/grub
Editer ce fichier pour modifier un parametre comme GRUB-TIMEOUT et ensuite excecuter la commande suivante
#grub2-mkconfig
L'equivalent de cette commande pour Debian est
#update-grub

Interaction avec l'amorceur de demarrage

Pour demarrer notre machine en rescue.target
A l'affichage de grub menu pressez [E] et rechercher la ligne linux, ensuite a la fin de cette ligne ajouter:
--> systemd.unit=rescue.target puis pressez [F10]

102.3 Gestion des bibliothèques partagées

Les bibliothèques partagées contiennent des fonctionalites que les autres applications peuvent utiliser et leur extension est .so.
Elles sont en general sauvegardees dans les repertoires suivants:
/lib
/usr/lib(32 bits) ou /usr/lib64(64bits)
/usr/share

Nous avons deux types de bibliothèques partagées:
        .Dynamic(extension .so)
        .Static(extension .a)

Management des bibliothèques partagées

#ldd [nom_programme]
Affiche toutes les bibliothèques partagées d'une commande ou programme exple: $ldd /usr/local/bin/python3.6

#ldconfig
Cree les liens des repertoires contenant des recentes bibliothèques partagées et les copie dans le repertoire /etc/ld.so.conf.d/

102.4 Utilisation du gestionnaire de paquetage Debian [Poids=3]

->Installation, mise à jour et désinstallation des paquetages binaires Debian.
->Recherche des paquetages contenant des fichiers ou des bibliothèques spécifiques installés ou non.
->Obtention d'informations sur un paquetage Debian comme la version, le contenu, les dépendances, l'intégrité du paquetage, et l'état d'installation (que le paquetage soit installé ou non). 

Apt(Advanced Package Tool)
Fichier contenant les repertoires des sources des paquets a installer /etc/apt/sources.list

#apt-get update

#apt-get upgrade

#apt-get remove [paquet]

#apt-get purge [paquet]
Desinstalle un paquet et toutes ses dependances

#apt-get dist-upgrade
Mise a jour du systeme et de tous les paquets a la prochaine version du systeme

#apt-get download [paquet]

#apt-get cache search [paquet]
Permet de rechercher un paquet

#apt-cache show [paquet]
Affiche lesinfos basiques d'un paquet

#apt-cache showpkg [paquet]
Afiche plus de details techniques d'un paquet

--> Utilisation de dpkg
Installe les paquets avec l'extension .deb prealablement telecharges

#dpkg --info [paquet.deb]
Affiche les infos d'un paquet

#dpkg --status [paquet]
Affiche les infos mais avec moins de details

#dpkg -l [paquet]
Affiche infos sur paquet 

#dpkg -L
Affiche la liste de tous les paquets installes

#dpkg -i [paquet.deb]
Installe un paquet

#dpkg -L [paquet]
Affiche tous les repertoires de ce paquet

#dpkg -r [paquet]
Supprime un paquet mais laisse ses fichiers de configuration

#dpkg -P [paquet]
Supprime le paquet ainsi que ses fichiers de configuration

#dpkg -S [paquet]
Affiche repertoires et fichiers concernes par ce paquet

#dpkg-reconfigure
Autorise la modification en reexecutant ses fichiers d'application exple $dpkg console-setup

#dpkg --forcedepends [paquet]
Force l'installation d'un paquet mais avec ses dependances manquantes

102.5 Utilisation des gestionnaires de paquetage RPM et YUM[Poids=3]
    
    -->Installation, réinstallation, mise à jour et suppression des paquetages avec RPM et YUM. 
    -->Obtention d'informations sur un paquetage RPM comme la version, le contenu, les dépendances, l'intégrité du paquetage, la signature et l'état d'installation.
    -->Détermination des fichiers relatifs à un paquetage donné, et recherche du paquetage auquel appartient un fichier donné. 

Yum(Yellowdog Upadater and Modified)

Fichier global de configuration de Yum est: /etc/yum.conf
Repertoires de Yum : /etc/yumrepos.d/

#yum update

#yum search [paquet]

#yum info [paquet]  

#yum list installed
Affiche la liste de tous les paquets installes

#yum clean all
Nettoie le cache pour les paquets a installer

#yum install [paquet]

#yum remove [paquet]
Desinstalle un paquet

#yum autoremove
Desinstalle tous les paquets non necessaires et leurs dependances

#yum whatprovides [paquet]
Affiche tous les repertoires concernes par ce paquet

#yum reinstall [paquet]
Reinstall un paquet

#yumdownloader [paquet]
Telecharge un paquet

#yumdownloader --urls [paquet]
Affiche le lien du download

#yumdownloader --destdir [paquet]
Indique le repertoire dans lequel le fichier sera telecharge

#yumdownloader --resolve [paquet]
Resoud tous les problemes de dependances liees a ce paquet.


Rpm(Red Hat Package Manager)

La base de donnees de rpm est localisee dans le dossier suivant: /var/lib/rpm

!Dans le cas ou notre base de donnees de rpm est corrompue, nous pouvons resoudre ce probleme par:
#rpm --rebuilddb

#rpm -qpi [paquet]
Affiche les infos d'un paquet

#rpm -qpl [paquet]
Affiche la liste des fichiers de configuration d'un paquet

#rpm -qa
Affiche la liste de tous les paquets installes

#rpm -ivh [paquet.rpm]
Installe un paquet

#rpm -U [paquet]
Mise a jour d'un paquet

#rpm -e paquet
Desinstalle un paquet

#rpm -Va
Verifie tous les paquets installes(M-> difference de mode, S-> difference de la taille , C-> fichier de configuration, g-> ghost file)

#rpm2cpio
Converti un fichier rpm en cpio exple $rpm2cpio nano-2.3.1-10.el7.x86_64.rpm | cpio -idmv (conserve les permissions, la version etc...)

102.6 Linux comme une machine virtuelle

TOPIC 103: Commandes GNU et Unix

103.1 Travail en ligne de commande(4)

-->Utilisation de commandes ou de séquences de commandes pour réaliser des tâches simples en ligne de commande.
-->Utilisation et modification de l'environnement du shell, en particulier la définition, l'export et le référencement des variables d'environnement.
-->Utilisation et édition de l'historique des commandes.
-->Exécution des commandes comprises ou non dans le chemin (path) par défaut. 

Linux shells
-->Bash(bourne again shell)
-->csh(Langage C style de syntaxe)
-->ksh(KornShell, base sous le bash avec des fonctionalites du C shelle ajoute)
-->zsh(Z inclut tous les elements de bash et ksh)

#env
Affiche toute la liste de mes variables d'environnement

#echo $[NOM_VARIABLE](en majuscule)
Affiche la valeur cette variable d'environnement

#set
Affiche toute la liste de mes variables d'environnement

#unset
Supprime une variable ou une fonction bash

#shopt
Affiche toutes les options de notre shell courant et leurs valeurs

#shopt -s [variable_shell]
Modifie la valeur de notre variable shell exple $shopt -s hostcomplete

#export 
Commande utilisee pour une nouvelle variable d'environnement dans notre shell courant exple $export HISTSIZE=3000

#pwd

#which

#type
Affiche le type du parametre passe qui peut etre fichier, alias, built-in, etc

Historic de Bash et Manuel d'aides

#history

Les pages du manuel sont divisees en plusieurs sections

section1:Programmes excecutables ou commandes shell
section2: les appels systemes fonctions fournies par le noyau
section3: les appels librairies fonctions des librairies des programmes
section4: fichiers speciaux en general ceux dans le fichier /dev
section5: Format des fichiers et conventions
section6: Jeux
section7: Divers
section8: Commandes de l'administration du systeme
Section9: les routines du noyau

#man -k [commande]
Affiche toutes les sections du manuel relatives a cette commande

#apropos
Affiche toutes les sections du manuel relatives a cette commande


103.2 Traitement de flux de type texte avec des filtres

Envoi de fichiers textes ou de sorties de commandes à des filtres textuels pour les modifier en utilisant des commandes UNIX appartenant au paquetage GNU textutils. 


#cat
Affiche le contenu d'in fichier texte
#less
Affiche le contenu d'in fichier texte avec possibilite de naviguer entre les lignes.

#head
Affiche les premieres lignes d'un fichier texte

#tail
Affiche les dernieres lignes d'un fichier texte 

#zcat
Affiche le contenu d'un fichier gz.

#bzcat
Affiche le contenu d'un fichier compresse de format bz2

 #xzcat
 Affiche le comtenu d'un dossier compresse

Statistiques des fichiers texte

#nl
Affiche le nombre de lignes d'un fichier texte

#wc
Affiche le nombre de mots d'un fichier exple: $wc -w text.txt
wc -l text.txt(affiche le nombre de lignes)

#od
Afficher le contenu d'un fichier en octal ou sous d'autres formats.  

Message Digests

#md5sum
Calcule la somme de compression d'un fichier base sur MD5 exple: 1) md5sum text.txt > text.md5 2)Modifier le fichier 3) verifier par $md5sum -c text.md5

#sha256sum
Calcule la somme de compression d'un fichier base sur SHA256

MANIPULATION DE TEXTE

#sort 
Permet de trier les lignes d'un fichier texte exple $sort -n text.txt
$sort -t "," -k2 text.txt(trie par ordre alphabetique le second element k2 delimite par le symbole ",")

#uniq
Eliminer les lignes dupliquées dans un fichier trié. Exple: $uniq -c text.txt(affiche le nombre d'occurence élément)
exple: uniq --group text.txt(Affiche les entrees identiques en les separant en groupe)

#tr
Transposer ou éliminer des caractères. Exple: cat text.txt | tr ',' ':'(remplace tous les caracteres , par :)

#cut
Supprime une partie de chaque ligne d'un fichier. Exple: $cut -d ':' /etc/passwd -f1

#paste
Regrouper les lignes de différents fichiers. exple: paste -d '-' text1.txt text2.txt(Regroupe ces deux fichiers en separant leur contenu respectif par -)

#sed
sed est un éditeur de flux. Un éditeur de flux est utilisé pour effectuer des transformations de texte basiques sur un flux d'entrée (un fichier ou l'entrée d'un tube).
exple: sed 's/windows/gnu-linux/g' text.txt(Remplace tous les windows par gnu-linux).
L'option -i de sed permet de modifier le fichier permanemment.

#split
Découper un fichier en différentes partie.  Exple: $split -b 100 text.txt(Divise le fichier text.txt en plusieurs fichiers de 100 bytes)
$split -d --verbose -n2 text.txt(Cree deux fichiers n2 dont le nom respectera un ordre numerique -d --verbose pour afficher les details.)

103.3 Gestion élémentaire des fichiers[Poids=4]

-/- Copie, déplacement et suppression des fichiers ou des répertoires individuellement.
-/- Copie récursive de plusieurs fichiers et répertoires.
-/- Suppression récursive de fichiers et répertoires.
-/- Utilisation simple et avancée des caractères génériques (wildcard) dans les commandes.
-/- Utilisation de find pour localiser et agir sur des fichiers en se basant sur leurs types, leurs tailles ou leurs temps (de création, modification ou accès).
-/- Utilisation des commandes tar, cpio et dd. 

#ls
ls, dir, vdir - Afficher le contenu d'un répertoire.
Exple: ls -lR /etc/ (Affiche le dossier et ses sous-dossiers) 

#touch
Modifier l'horodatage d'un fichier. Exple: touch -m text.txt(Change l'horodatage du fichier au temps courant)

#cp

#rm

#mv

#file
Déterminer le type d'un fichier.

Manipulation de repertoires
---------------------------

#cd
Permet d'acceder a un repertoire Exple: $cd - ( Permet de retourner au repertoire precedent si la variable $OLDPWD est configuree)

#mkdir
Créer des répertoires. Exple: $mkdir -p dossier/sous-dossier(Permet de creer dossier et son sous-dossier)

#rmdir
Permet de supprimer un dossier vide. Exple: $rm -r (Permet de supprimer un dossier non vide)


#find
Rechercher des fichiers dans une hiérarchie de répertoires.
Exple: $find / -name "test"(Recherche dans le repertoire / tous les fichiers et dossiers contenant 'test')
       $find / -atime 10 (Recherche tous les fichiers qui ont ete modifie pendant ces dix dernieres heures)
       $find / -cmin 5 (Permet de rechercher tous les fichiers et dossiers modifies ces cinq dernieres minutes )
       $find /var -name "*.log" -group nginx (Permet de rechercher dans le repertoire /var tous les fichiers ayant l'extension .log modifies par le groupe nginx)
       $find /home/usr/bin -name "*.sh" -exec cp -f {} /home/user/sauvegarde/bin \; (Permet de rechercher tous les fichiers .sh et excecute la commande de copie de ses fichiers dans le second repertoire indique).
       $find / . -ctime 1 (Permet de rechercher tous les fichiers modifies hier, periode de 24 c-a-d deux jours ===> ctime 2)
       $find /home/yankees -newer passwd (Permet d'afficher tous les fichiers crees plus recent que passwd)
       $find /home/yankees -empty (Permet de rechercher tous les dossiers vides dans le repertoire indique)
       $find /home/yankees -empty -type f (Permet de rechercher tous les fichiers vide dans le repertoire indique)
       $find /home/yankees -empty -type -exec rm -f {} \; (Permet de rechercher tous les fichiers vides et les supprimes)
       $find /home/yankees -name "*.tar.*" -exec cp -v {} /home/yankees/liste_fichiers_compresses \;(Permet de rechercher la liste de tous les fichiers compresses contenant tar et copie leurs noms dans le fichier liste_fichiers_compresses)



Compression/Decompression de fichiers et dossiers
-------------------------------------------------

#dd
Copie un fichier (par défaut, depuis l'entrée standard vers la sortie standard) en permettant de sélectionner la taille de bloc, et d'effectuer des conversions. 
Exple: $dd if=/dev/sda of=/home/yankees/sauvegarde.img count=1 bs=512(Permet de faire la sauvegarde de /dev/sda en effectuant la copie du premier block de 512 bytes qui en realite represente notre master boot record (MBR))
       $dd if=/dev/sr0 of=/home/yankee/cdimage.iso (Permet de sauvegarde le contenu du CD dans un fichier cdimage.iso)
       $dd if=/dev/urandom of=fichier_test bs=1024k count=10(Permet la copie de donnees arbitraire de 1024k=1M * 10 = 10MB dans le fichier fichier_test )
       N.B: Vous pouvez restorer votre sauvegarde en permutant les valeurs de if and of.

#tar
la version GNU de l'utilitaire tar de gestion d'archives. 
Exple: $tar -cf dossier_compresse.tar dossier_a_compresse/ (Permet de creer un fichier compresse) 
       $tar -t dossier_compresse.tar (Permet de lister le contenu de notre dossier compresse)
       $tar -xf dossier_compresse.tar (Permet de decompresse notre fichier)
       $tar -czf dossier_compresse.tar.gz dossier_a_compresse/ (Permet de creer un fichier compresse de .gz avec l'algorithme de compression bzip)
       $tar -cvjf dossier_compresse.tar.bz2 /home/yankees/ (Permet de creer un fichier compresse de type bz2 de tout le dossier de l'utilisateur yankees) 

#gzip
Compacter ou décompacter des fichiers.  
Exple: $gzip dossier_a_compresse (Permet de compacter notre dossier)
       
#gunzip
#bzip2
#bunzip2

#xz
Nouvel utilitaire de compression et decompression sous GNU/Linux avec de meilleures performances
Exple: $xz dossier_a_compresse (Compresse un dossier)

#unxz
Permet de decompresser un fichier de type .xz

File Globbing
-------------

*(Tous les caracteres possibles)
Exple: $ls *.txt(Recherche tous les caracteres possible situes avant .txt)
Exple: $ls text*.(Recherche tous les caracteres possible apres text)

?(un seul caractere possible)
Exple: $ls ?ext.txt(Recherche un fichier dont le nom commence par la lettre t)
       $ls ??xt.txt
       $ls [Tt]*.txt(Recherche tous les fichiers commencant par T ou t suivis de toutes les combinaisons possibles mais se terminant par.txt)
       $ls [Dd]ocument[Rr]apport200[0-9]?2019*
[^abc](Tous les fichiers ne commencant pas a mais contenant bc)


103.4 Utilisation des flux, des tubes et des redirections[Poids=4]

-/-Redirection de l'entrée standard, de la sortie standard et de l'erreur standard.
-/-Connexion de la sortie d'une commande à l'entrée d'une autre commande.
-/-Utilisation de la sortie d'une commande comme paramètres d'une autre commande.
-/-Envoi simultané du résultat d'une commande vers la sortie standard et vers un fichier. 

Redirection de  la sortie standard(stdout -- 0) : >, >>
Redirection de l'entrée standard(stdin -- 1) : >, |
Redirection de l'erreur standard(stderr -- 2) : 2>

Exple: $cat /var/log/nginx | more
       $find /user -name "*.sh" > sortie.txt
       $find /user -name "*.txt" >> sortie.txt
       $cat < sortie.txt <==> cat sortie.txt
       $cat /var/log/auth.log 2> /dev/null(Afficher le contenu du fichier auth.log mais ne pas afficher tous messages d'erreur de cette commande seul root)
       $cat /var/log/auth.log 2> /dev/null > erreur.txt(Ne pas afficher l'erreur mais plutot le sauvegarder dans un fichier erreur.txt)
       $cat /var/log/auth.log > /dev/null 2>&1 (Ne pas afficher l'erreur et la sortie standard de cette commande)

#tee
Copier l'entrée standard sur la sortie standard et dans un fichier.
Exple: $ls -ld /usr/share/doc/lib[Xx]* | tee liste_dossiers_libx.txt(Affiche tous les dossiers contenant libx or libX mais sauvegarder le resultat de la commande dans le fichier)
       $ls -ld /usr/share/doc/lib[Xx]* | tee liste_dossiers_libx.txt | sort -r | tee liste_dossiers_libx_renverses.txt(Plusieurs tee )

#xargs
construire et exécuter des lignes de commandes à partir de l'entrée standard.
Exple: $ find /home/yankees/ -empty | xargs rm -rf (Recherche tous les dossiers et fichiers vides et les supprime avec la commande xargs) 
       $ grep -l "DB" /home/yankees/Documents/TUTORIALS/*.sql | xargs -I {} mv {} /home/yankees/Documents/TUTORIALS/BAK/ (Affiche tous les fichiers ayant pour extension .sql contenant DB et les copier dans le dossier BAK)
       $find ~ -name "*.sh" | xargs ls -al > scripts.txt()


103.5 Création, contrôle et interruption des processus[Poids=4]

-/-Exécution de tâches au premier plan et en arrière plan.
-/-Indiquer à un programme qu'il doit continuer à s'exécuter après la déconnexion.
-/-Contrôle des processus actifs.
-/-Sélection et tri des processus à afficher.
-/-Envoi de signaux aux processus. 

Notions basiques d'un processus

#ps
 Afficher l'état des processus en cours. 
 Exple: $ ps -u nomUtilisateur (Affiche tous les processus inities par un utilisateur)
        $ ps -eH (Affiche tous les processus mais de facon hierachique)
        $ ps -efH (Affiche tous les processus avec leurs arguments)
N.B: Toutes les infos de ps proviennent de /proc

Contrôle des processus
----------------------

#uptime
Affiche sur une ligne les informations suivantes : L'heure actuelle, la durée depuis laquelle le système fonctionne, le nombre d'utilisateurs actuellement connectés, et la charge système moyenne pour les 1, 5, et 15 dernières minutes. 

#free
Afficher les quantités de mémoires libres et utilisées. Exple: $ free -h (Affiche de facon claire la taille de la memoire, tampon aussi)

#pgrep
Affiche tous les processus actifs et leurs PID selon votre critere de recherche.
Exple: $ pgrep sshd
       $ pgrep -a sshd
       $ pgrep -u nomUtilisateur sshd
       $ pgrep -au nomUtilisateur (Affiche tous les processus actifs de cet utilisateur avec les details)

#kill
Envoyer un signal à un processus.  

 Les signaux standards
 SIGKILL       9       Term    Kill signal (Termine de facon violente un processus)
 SIGTERM      15       Term    Termination signal (Tue proprement un processus en nettoyant ses fichiers, etc)

Exple: $ sudo kill PID 
       $ kill -l (Affiche tous les signaux possibles)
       $ sudo kill -9 PID
       $ sudo kill -15 PID

#pkill
Verifie ou envoie un signal a un processus en fonction du nom ou encore d'autres parametres de recherche.
Exple: $ sudo pkill httpd (Termine le processus httpd et les sous-processus)
       $ sudo pkill -x httpd (Termine seulement le processus ayant le httpd et non les sous-processus de ce dernier)

#killall
Envoyer un signal à des processus indiqués par leurs noms.  
Exple: $ sudo killall sshd
       $ sudo killall -s 15 apache2

#watch
Excecute une commande de facon periodique et affiche la sortie.
Exple: $ watch -n 5 date (Affiche la date chaque 5 secondes)

#screen
Est un « multiplexeur de terminaux » permettant d'ouvrir plusieurs terminaux dans une même console, de passer de l'un à l'autre et de les récupérer plus tard. 
Scenario:
        $ screen -S htop
        $ htop
        ctrl + a + d (Pour se detacher de la session)
        $ screen -S top
        $ top
        ctrl + a + d (Pour se detacher de la session)
        $ screen -ls (Affiche toutes les sessions)
        $ screen -r [numero_session]
        $ exit (Pour terminer la session)
Scenario: avec des connexion ssh des servers

#tmux
Est un « multiplexeur de terminaux » permettant d'ouvrir plusieurs terminaux dans une même console.

ctrl + d + b (Pour se detacher d'une session tmux)
$ tmux ls (Affiche toutes les sessions)
$ tmux attach-session -t [numero_session]

#nohup
Exécute la commande désirée en ignorant les signaux HANGUP (déconnexion), avec une priorité d'ordonnancement incrémentée de 5, afin que cette commande continue à s'exécuter en arrière-plan après la déconnexion de l'utilisateur. 
Exple: $ nohup ping www.attecoube.net & (Effectue la commande ping meme en etant deconnecte de la session terminal et cree un fichier [nohup.out]pour sauvegarder la sortie de cette commande)

#jobs
Permet de lister tous les processus s'exécutant en arrière-plan.

#bg
Exécute la commande en arrière-plan

#fg
Exécute la commande en avant-plan


103.6 Modification des priorités des processus[Poids=2]

-/-Connaissance de la priorité par défaut affectée à un nouveau processus.
-/-Exécution de programme avec une priorité plus haute ou plus basse que celle par défaut.
-/-Changement de la priorité d'un processus en cours d'exécution. 

## -20 (Valeur la plus elevee d'une priorité)
## 19 (La plus faible valeur d'une priorité )
## 0 (Valeur par defaut d'une priorité)
## Modifiable par le root

##N.B: $ps -o pid,nice,cmd,user (Permet de specifier les details de la commande ps)

#nice
Exécuter un programme avec une priorité d'ordonnancement modifiée. 
Scenario
        $ ps -o pid,nice,cmd,user
        $ watch -n 5 date & (Permet d'executer la commande date chaque 5 secondes mais en arrière-plan )
        $ ps -o pid,nice,cmd,user (Afficher de nouveau tous les processus)
        $ kill -9 PID (Arreter le processus watch)
        $ nice -n 5 watch -n 5 date & (Permet d'executer la commande date chaque 5 secondes mais en arrière-plan mais cette en diminuant son niveau de priorité à 5 )

#renice
Modifier un programme en cours d'exécution avec une nouvelle priorité d'ordonnancement.
Exple: $ sudo renice -n -3 PID

#top
Exple: $ top -i (Affiche les processus actifs)
       $ top -d [temps_secondes] (Affiche les processus actifs chaque secondes definis)


103.7 Recherche dans des fichiers texte avec les expressions rationnelles[Poids=3]

-/-Création d'expressions rationnelles simples contenant différents éléments de notation.
-/-Utilisation des expressions rationnelles dans des commandes pour effectuer des recherches dans une arborescence ou dans le contenu d'un fichier. 

.(Represente un seul charactere)
^(Represente le debut d'une ligne)
? (Represente un caractere optionel, mais seulement un seul)
+ (doit correspondre a au moins un seul caractere mais peut avoir plusieurs valeurs )
{#} (correspond au nombre de fois d'un caractere)
{#,} (Correspond a un caractere ou plus)
{#,#} (correspond a une occurence minimum ou maximum de fois exple {1,3} min=1 max=2)
\> (mot qui commence par ce qui suit apres ces symboles)
^ (mot qui commence par definit apres ce symbole)
[^] (mot qui ne contient pas cette lettre mentionnee apres le symbole)
$(Utilise pour la fin d'une ligne)
[abc](Recherche d'une charactere special)
*(Rechercher plus d'un caractere precedent le sysmbole)

Exple: $ grep ^nk /etc/passwd (Recherche toutes les lignes commencant par nk)
       $ grep nke$ /etc/passwd (Recherche toutes les lignes se terminant par nke)
       $ grep ^[Aa].[Aa][^h]

Utilisation des outils pour les expressions rationnelles

#sed
sed est un éditeur de flux. Un éditeur de flux est utilisé pour effectuer des transformations de texte basiques sur un flux d'entrée (un fichier ou l'entrée d'un tube).
sed est un éditeur de flux. Un éditeur de flux est utilisé pour effectuer des transformations de texte basiques sur un flux d'entrée (un fichier ou l'entrée d'un tube).

Exple:
$ cat /etc/passwd | sed '/sync$/p' (Affiche toutes les lignes qui n'ont pas 'sync' comme fin de ligne)

#egrep
C'est une variante de la commande grep mais sans l'utilisation de l'option -E qui favorise l'utilisation d'expressions rationnelles.
Exple: $ egrep  'nologin$' /etc/passwd (Affiche toutes les lignes dont la fin contiennent 'nologin')
       $ egrep -c 'nologin$' /etc/passwd (Affiche uniquement le nombre d'occurences de lignes dont leur fin est marque par 'nologin')
       $ egrep 'bash$|^nke' /etc/passwd (Affiche toues les lignes se terminant par 'nologin' et commencant par 'nke')
       $ fgrep -f liste_caracteres.txt /etc/passwd (Permet de rechercher toutes les lignes contenant les caracteres specifies dans le ficher liste_caracteres.txt)
       $ grep ^http[^x] /etc/services > http-services (Recherche toutes les lignes commencant par http mais ne contenant pas 'x' a la fin )
       $ grep ^ldap.[^a] /etc/services > ldap.txt (Recherche toutes les lignes commencant par ldap mais la cinquieme caractere ne commence pas par 'a')
       $ grep -v services$ https-services.txt > http-updated.txt (Copie l'oppose de toutes les lignes contenant 'services' a la fin)

103.8 Édition de fichiers texte avec vi

-/-Déplacement dans un document édité avec vi.
-/-Utilisation des modes de base de vi.
-/-Insertion, modification, suppression, copie et recherche de texte. 

#Mode Commande
        i - invoke the 'insert mode' at the current cursor position where you can begin typing in the document
        • I - move to the beginning of the current line and invoke 'insert mode'
        • a - invoke insert mode, placing the cursor one character to the right of the current position (append)
        • A - move to the end of the current line, placing the cursor one character to the right of the ending position (line append)
        • o - insert a new line under the current line, place the cursor in the first position on the new line in 'insert mode'
        • O - insert a new line above the current line, place the cursor in the first position of the newline in 'insert mode'
        • c[option] - change the text at the current position
        • cw - change the word at the current position
        • cc - change the line at the current position
        • c$ - change from the current position to the end of the line
        • r - replace the character at the current position
        • R - replace text on the same line until you escape the 'insert mode' or until you reach end of line
        • x - delete the character after the cursor
        • X - delete the character before the cursor
        • dw - delete the word after the cursor
        • dd - delete the entire line the cursor is on
        • D - delete the text from the current cursor to end of line
        • dL - delete the text from the current cursor to the end of the current screen
        • dG - delete the text from the current cursor to the end of the file
        • d^ - delete all text from the beginning of line to the current cursor
        • u - undo the last operation/change
        • yy - copy the current line to the buffer (often called yank)
        •yw - copy from current cursor to end of current word
        • p - paste contents of the buffer after the cursor
        • P - paste the contents of the buffer before the cursor
        • :e! - undo ALL changes since the last time the file was saved to disk
        • :w - write the file to disk (save)
        • :q - quit the editor (will warn you if the file has changed and not saved)
        • :q! - quit right now, don't worry about if it was changed and saved
        • :x - shortcut for save and exit
        • ZZ - shortcut for save and exit

#Raccourci pour le mode Navigation 
        • h - one character left
        • j - one line down
        • k - one line up
        • l - one character right

#Notes: any of the above can be repeated by putting the desired number in front
        •For example - 3k (would move 3 lines up)
                        2h (would move 2 characters left)
        • ctl-u - move back one half page
        • ctl-b - move back one page
        • ctl-d - move forward one half page
        • ctl-f - move forward one page
        • ctl-G - show the name of the file, lines and position in percentage of the total file length
        • [#]G - move directly to the indicated line
        • [#]W - move 12 words to the right
#Mode Recherche
        • Must be in command mode (press ESC key to make sure you are in command mode)
        • /[string] - search from cursor position forward for 'string'

        •?[string] - search from cursor position back for 'string'

        •N - when used after a search, will find the 'next' occurence of said 'string' in indicated direction

#Remplacement 
        • must be in command mode (press ESC key to make sure you are in command mode)
        • sed-like syntax
        • s - substitute (in the current line)
        %s - substitute (in the entire file)
        • /[value to find] - what to search for
        • /[value to substitute]/ - what to replace with
        • g - optional, will replace ALL occurrences rather that just the first
        •
        For example - :s/Mar/Apr/g (Remplacer toutes les occurences de Mar par Apr)

#Execution de commande
        •:! [cmd] - run the indicated command on the command line
2
TOPIC 104 : Disques, systèmes de fichiers Linux , arborescence de fichiers standard (FHS) 

104.1 Création des partitions et des systèmes de fichiers[Poids=2]

-/-Gestion des tables de partition MBR
-/-Utilisation des différentes commandes mkfs pour le paramétrage des partitions et la création des différents systèmes de fichiers comme :
        -ext2/ext3/ext4
        -XFS
        -VFAT
-/-Sensibilisation à ReiserFS et Btrfs
-/-Connaissance de base de gdisk et parted avec les partitions GPT.


Types de Partitions
-------------------
8200 - Linux swap
8300 - Linux(ext2, ext3, etc...)
8301 - Partition linux reserve
8e00 - Linux LVM
fd00 - Linux RAID

Types de systemes de fichiers
-----------------------------

ext2 - Linux extended filesystem (legacy)
ext3 - Linux extended filesystem with journaling (logging capability for easier and quicker recovery from disk issues)
ext4 - Linux extended filesystem with journaling (including performance enhancements over ext3)
xfs - extent filesystem, enhanced performance, particularly on filesystems with many smaller files
ReiserFS - one of the first filesystems to introduce journaling and offer dynamic resizing capabilities
btrfs - builds on ReiserFS features while adding additional admin features while increasing performance on larger filesystems
iso9660 - filesystem specific to CD-ROM
udf - filesystem specific to DVD
vfat - older DOS partition type (used for compatibility with other operating systems)


#fdisk 
fdisk est un programme piloté par menu utilisé pour la création et la manipulation de tables de partitions. Il comprend les tables de partitions de type DOS, et les labels de disque BSD ou SUN.

#parted

GPT Partitions

#gdisk

Swap Partitions

#mkswap
Configure une partition en mode swap.
Exple: # mkswap -L BCKSWAP /dev/sda10 (Cree une partition swap nomme BCKSWAP sur la partition /dev/sda10)

#swapon
Permet d'activer une partition swap pour usage. Exple: # swapon -L BCKSWAP (Active notre partition swap nommee BCKSWAP)

#swapoff
Permet de desactiver une partition swap. Exple: # swapoff -L BCKSWAP 

#mkfs
mkfs est utilisé pour formater un système de fichiers Linux sur un périphérique, généralement une partition de disque dur.
Exple: # mkfs -t ext4 /dev/sda12 (Permet de creer un systeme de fichier de type ext4 sur la partition /dev/sda12)
       #mkfs.ext4 -L SvrUbuntu /dev/sda12 (Permet de creer un systeme de fichier de type ext4 nomme SrvUbuntu sur la partition /dev/sda12)


104.2 Maintenance de l'intégrité des systèmes de fichiers[Poids=2]

-/-Vérification de l'intégrité des systèmes de fichiers.
-/-Contrôle de l'espace et des inodes libres.
-/-Réparation de problèmes élémentaires sur les système de fichiers. 

#df
Fournit la quantité d'espace occupé des systèmes de fichiers. 
Exple: $ df -h (Affiche la quantite dans un format lisible pour u humain)
       $ df --total -h
#du
 affiche la quantité d'espace disque utilisée par chacun des arguments, et pour chaque sous-répertoire des répertoires indiqués en argument.
 Exple: $ du -h
        $ du -sh /home (Affiche la quantité totale d'espace du repertoire /home)
        $ du -h --max-depth=3 /etc/ (Affiche la quantité totale d'espace du repertoire /etc mais en se limitant a trois sous-repertoires)

Notes:
------
Tout fichier possède son unique inode. L'inode contient la totalité des informations sur le fichier, sauf le nom et ont tous de la même taille.
Les informations de l'inode peuvent etre:

    Type de fichier : -,d, l, c, p, b.
    Droits d'accès : par exemple : rwxr-x---
    Nombre de liens (physiques) : correspond au nombre de références c'est à dire au nombre de noms.
    UID : effectif du processus créateur ou affecté par chown.
    GID : effectif du processus créateur, affecté par chgrp ou hérité du répertoire.
    Taille du fichier.
    atime :date de la dernière lecture.
    mtime :date de la dernière modification.
    ctime :date de la dernière connexion.
    Adresse du fichier. 

Exple:
$ df -i (Permet d'afficher le nombre total d'inodes pour un emplacement)
$ ls -il (Affiche le numero inode de tous les fichiers et dossiers du repertoire)
$ du --inode /etc (Affiche le nombre inodes utilises dans le repertoire /etc/)

#fsck
Est utilisé pour vérifier et optionnellement réparer un ou plusieurs systèmes de fichiers Linux.
Exple: # fsck -r /dev/sda12 (Permet d'afficher un rapport sur l'etat de cette partition)

#e2fsck
Est utilisé pour vérifier et optionnellement réparer un ou plusieurs systèmes de fichiers Linux.
Exple: # e2fsck -f /dev/sda12 (Permet de forcer la verification d'une partition memem si celle semble "clean")

#mk2fs
Est utilisé pour créer un système de fichiers Linux.
Exple: # mk2fs -t ext4 -L BACKUP /dev/sdb1 (Permet de creer un système de fichiers de type -ext4 et dont le label est BACKUP)

#tune2fs
Est utilise pour ajuster les parametres d'un systeme de fichier.
Exple: # tune2fs -i 4w /dev/sdb1 (Permet de verifier l'integrite du systeme de fichier chaque 4 semaines(w))

#xfs_repair
Est utilisé pour reparer les systemes de fichiers de type XFS.

#xfs_fs
Est utilisé pour reorganiser les donnees stockees dans un systeme de fichier de type xfs, similaire a l'utilitaire de defragmentation sous Windows.

#xfs_db
Est utilisé pour debugger un systeme de fichier xfs

104.3 Montage et démontage des systèmes de fichiers[Poids=3]
-/-Montage et démontage manuel des systèmes de fichiers.
-/-Configuration du montage des systèmes de fichiers au démarrage du système.
-/-Configuration des options de montage des systèmes de fichiers. 

















































