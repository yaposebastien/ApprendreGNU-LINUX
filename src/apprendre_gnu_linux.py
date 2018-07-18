#!/usr/bin/env python3.6
from __future__ import absolute_import, division, print_function
import subprocess
import time


def MenuApprendre():
    print(f'\n\t Section I: Architecture du Systeme.')
    print(f'\n\t Pressez[1] Afficher le contenu de repertoire des infos du systeme.')

    choixUtilisateur = input('Saisir votre choix: ')
    
    return choixUtilisateur


def architectureSysteme():
    print('Le dossier "/proc" contient tous les fichiers des peripheriques')
    time.sleep(20)
    cont_proc = subprocess.run(['ls', '-l', '/proc'])
    print(cont_proc)






if __name__ == '__main__' :

    try:
        deContinuer = False
        while deContinuer == False:
            if MenuApprendre() == '1':
                architectureSysteme()

    except Exception as excpt:
        print(str(excpt.message))




