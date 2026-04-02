#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Name    : ma24_dames_rules.py
Authors : Pascal Benzonana and Vitor COVAL
Date    : 2025.01.17
Version : 0.05
Purpose : Librairie backend du jeu de dames développé dans le cadre
          du module MA-24

# ------------------------------------------------------------------------------
# Revisions
# ------------------------------------------------------------------------------

# 2025-01-17 05 VCL
  - Version évaluation du 17.01.2025

# 2025-01-15 04 VCL
  - Enlevé les fonctions : prend_piece()

# 2025-01-09 03 VCL
  - Ajouté les fonctions : dans_plateau, change_joueur, prend_piece,
    case_jouable, selectionnable.
    Version non fonctionnelle.

  2024-12-05 02 PBA & VCL
  - Ajouté les fonctions de déplacement haut, bas, gauche, droite

  2024-11-07 01 PBA & VCL
  - Version initiale
"""


def plateau(taille_plateau=(10,10)):
    """Définit la taille du plateau
    """
    global nb_lignes, nb_colonnes
    nb_colonnes = taille_plateau[0]
    nb_lignes = taille_plateau[1]


def plateau_vide():
    """ Crée et initialise le plateau
    """
    global plateau_board, nb_lignes, nb_colonnes, case_paire, case_impaire
    plateau_board = [1]*nb_lignes
    for ligne in range(nb_lignes):
        plateau_board[ligne] = [case_impaire, case_paire]*(nb_colonnes//2)\
            if not ligne % 2 else [case_paire, case_impaire]*(nb_colonnes//2)
        if nb_colonnes % 2:
            plateau_board[ligne] += [plateau_board[ligne][0]]

    # dessine le damier
    for ligne in range(nb_lignes):
        for col in range(nb_colonnes):
            #if dessine_case is not None:
            dessine_case(col, ligne, plateau_board[ligne][col])


def dans_plateau(posx, posy):
    """Fonction qui détermine si les positions passées en paramètres
        sont correctes (dans le plateau ou à l'extérieur)
    """
    global nb_lignes, nb_colonnes
    if 0 <= posx < nb_colonnes and 0 <= posy < nb_lignes:
        return True
    return False


def new_game():
    """
    """
    global plateau_board, nb_lignes, nb_colonnes
    plateau_vide()
    for ligne in range((nb_lignes-2)//2):
        for col in range(nb_colonnes):
            if plateau_board[ligne][col]:
                plateau_board[ligne][col] = JOUEUR_HAUT
                dessine_piece(col, ligne, JOUEUR_HAUT)
            if plateau_board[nb_lignes-1-ligne][col]:
                plateau_board[nb_lignes-1-ligne][col] = JOUEUR_BAS
                dessine_piece(col, nb_lignes-1-ligne, JOUEUR_BAS)


def change_joueur():
    """ Change les joueurs"""
    global joueur, autre_joueur
    joueur, autre_joueur = autre_joueur, joueur


def case_jouable(posx, posy):
    """Fonction qu'identifie si la case sélectionnée (posx, posy)
        contient un pion du joueur à qui c'est le tour de jouer
    """
    global joueur, autre_joueur, messages, plateau_board

    est_jouable = True  # Par défaut la case est jouable
    piece = plateau_board[posy][posx]
    if piece % joueur or not piece:
        # Pièce non jouable (autre joueur) ou case vide ou case blanche
        if piece % joueur:
            # La pièce ne corresponds pas au joueur
            est_jouable = False     # C'est au tour du premier joueur,
                                    # mais la case contient une pièce
                                    # du deuxième joueur
            messages += ["Mauvaise sélection de pièce, c'est à l'autre joueur\
                            de jouer"]
        elif piece and selection_multiple:
            # C'est une case vide, et on est en sélection multiple
            # A faire :
            # - Vérifier que la sélection première est une dame ou un pion
            # - Vérifier par rapport aux dernières sélections qu'il y a une pièce
            #   adverse entre ou que la case se trouve dans la liste des sélections
            #   multiples
            pass
        else:
            # C'est une case non jouable (blanche)
            est_jouable = False
    else:
        print("piece jouable ! (piece :", piece, ", joueur :", joueur,")")
    return est_jouable


def selectionable(posx, posy):
    """Fonction qu'identifie si la case sélectionnée (posx, posy)
        contient une pièce ou un espace intermédiaire qui peut être
        sélectionné pour le mouvement en cours
    """
    global selection_multiple, selections_multiple, prises_multiple, voisins
    est_selectionnable = True   # Définit par défaut que la position peut
                                # être jouée
    if not dans_plateau(posx, posy):
        deselectionne()
        return False

    if selection_multiple:
        # On se trouve dans une situation de sélection multiple (une
        # sélection a déjà été effectuée)
        if dans_plateau(posx, posy):
            print("Dans le plateau")
            oldx, oldy = selections_multiple[len(selections_multiple)-1]
            if (oldx, oldy) == (posx, posy):
                deselectionne()
                return False
            if avance_gauche(oldx, oldy) == (posx, posy) or avance_droite(oldx, oldy) == (posx, posy):
                bouge(posx, posy)
                selection_multiple = False
                selections_multiple = None
                change_joueur()
        else:   # Cliqué en dehors du plateau, désactiver la prise
                # multiple
            deselectionne()
            est_selectionnable = False
    elif len(voisins):
        # On se trouve dans un situation de prise simple avec des pièces
        # qui peuvent être prises dans la diagonale
        contenu_case = plateau_board[posx][posy]
        if contenu_case:    # Ne peut avoir que les valeurs 3, 4, 6 ou 8
            pass
    else:
        # On se trouve dans une situation de sélection simple sans
        # possibilité de prendre des pièces (juste avancer)

        # Vérification que c'est une pièce qui peut être jouée (pas
        # bloquée par d'autres pièces
        print("else_selectionnable")
        if peut_avancer(posx, posy):
            print("on selectionne la case")
            selection_multiple = True
            selections_multiple = [(posx, posy)]
            dessine_selection(posx, posy, "JOUEUR")
        else:
            est_selectionnable = False

    return est_selectionnable


def bouge(posx, posy):
    """Fonction qui déplace les pions dans les cases
    """
    global plateau_board, selections_multiple
    (oldx, oldy) = selections_multiple[len(selections_multiple)-1]
    plateau_board[posy][posx] = plateau_board[oldy][oldx]
    plateau_board[oldy][oldx] = 1
    dessine_case (oldx, oldy, 1)
    dessine_case (posx, posy, 1)
    dessine_piece (posx, posy, plateau_board[posy][posx])


def deselectionne():
    """Fonction qui enlève la sélection des cases précédement sélectionnées
    """
    global selection_multiple, selections_multiple, dessine_selection, case_blanche
    if selections_multiple is not None:
        for posx, posy in selections_multiple:
            if case_blanche:
                dessine_selection(posx, posy, "CASE BLANCHE")
            else:
                dessine_selection(posx, posy, "CASE NOIRE")

    selection_multiple = False
    selections_multiple = None


def avance_gauche(posx, posy):
    """Fonction sert à identifier si le joueur peut avancer sur la case
        de gauche. La fonction renvoie la position x, y si le joueur
        peut avancer à gauche, sinon, elle renvoie 'None'
    """
    global plateau_board, JOUEUR_BAS, nb_lignes, nb_colonnes
    piece = plateau_board[posy][posx]   # pion ou dame ?
    avance = None  # Par défaut la pièce ne peut pas avancer
    if piece % joueur:
        # La pièce est une dame
        pass
    else:
        # La pièce est un pion
        if joueur % JOUEUR_BAS:
            # On joue de haut en bas
            if posy < (nb_lignes-1):
                if posx < (nb_colonnes-1):
                    if plateau_board[posy+1][posx+1] == 1:
                        avance = (posx+2, posy+1)
        else:
            # On joue de bas en haut
            if posy > 0:
                if posx > 0:
                    if plateau_board[posy-1][posx-1] == 1:
                        avance = (posx-1, posy-1)
    return avance


def avance_droite(posx, posy):
    """Fonction sert à identifier si le joueur peut avancer sur la case
        de droite. La fonction renvoie la position x, y si le joueur
        peut avancer à droite, sinon, elle renvoie 'None'
    """
    global plateau_board, JOUEUR_BAS, nb_lignes, nb_colonnes
    piece = plateau_board[posy][posx]   # pion ou dame ?
    avance = None  # Par défaut la pièce ne peut pas avancer
    if piece % joueur:
        # La pièce est une dame
        pass
    else:
        # La pièce est un pion
        if joueur % JOUEUR_BAS:
            # On joue de haut en bas
            if posy < (nb_lignes-1):
                if posx > 0:
                    if plateau_board[posy+1][posx-1] == 1:
                        avance = (posx-1, posy+1)
        else:
            # On joue de bas en haut
            if posy > 0:
                if posx < (nb_colonnes-1):
                    if plateau_board[posy-1][posx+1] == 1:
                        avance = (posx+1, posy-1)
    return avance


def peut_avancer(posx, posy):
    """Détermine si la pièce peut avancer ou pas
    """
    if avance_gauche(posx, posy) or avance_droite(posx, posy) is not None:
        return True
    return False


# Identification des joueurs, pions, dames et couleurs :
# L'idée consiste à identifier les dames avec une valeur double de
# celle des pions. Les pions avec la même valeur que le joueur.
# Ainsi, lorsque ce sera le tour du joueur à jouer, on validera que
# la pièce qu'il veut déplacer est une de ses pièces avec une fonction
# modulo (le résultat donnera toujours 0).
# Les deux joueurs ne doivent pas avoir des nombres multiples communs
# sinon les fonctions mathématiques devront être plus complexes.
# On choisi les valeurs 3 et 4 pour chaque joueur.
JOUEUR_BAS = 3  # Détermination des valeurs :
JOUEUR_HAUT = 4      #  - 3 : pion du joueur du bas du plateau
                #  - 4 : pion du joueur du haut du plateau
                #  - 6 : Dame du joueur du bas du plateau
                #  - 8 : Dame du joueur du haut du plateau

# Variables joueur
blancs = JOUEUR_BAS          # Définit que les blancs sont en bas
joueur = JOUEUR_BAS          # Définit le premier joueur
autre_joueur = JOUEUR_HAUT   # Définit le deuxième joueur

# Variables des cases
case_paire = 0              # Définit les cases paires vides par défaut
case_impaire = 1            # Définit les cases impaires comme cases
                            # de jeu par défaut (en bas à gauche sur le
                            # plateau)
case_blanche = case_paire   # Définit les cases blanches sur les cases
                            # paires par défaut
case_noire = case_impaire   # Définit les cases noires noires sur les
                            # cases impaires par défaut

dessine_case = None     # Callback pour dessiner les cases
dessine_piece = None    # Callback pour dessiner la pièce (pion/dame)
dessine_selection = None    # Callback pour dessiner la selection d'une
                            # case ou d'une pièce

mouvements = []         # Historique des parties
pion_pos = None         # Positions en [x, y]
nb_lignes = 10          # Définit le nombre de lignes du plateau
nb_colonnes = 10        # Définit le nombre de colonnes du plateau
plateau_board = None    # Contient les pièces sur le plateau
selection_multiple = False  # Identifie si le joueur est entrain de choisir
                            # le chemin à utiliser pour les prises
selections_multiple = None  # Utilisé pour garder en mémoire les
                            # sélections multiples
voisins = {}            # Utilisé pour identifier s'il y a des prises
                        # et quelles sont-elles
plateau()

messages = list()