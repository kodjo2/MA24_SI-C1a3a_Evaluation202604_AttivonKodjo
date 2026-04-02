#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Name    : ma24_dames_gfx.py
Authors : Attivon Kodjo
Date    : 02.04.2026
Version : 0.06
Purpose : Librairie graphique du jeu de dames développé dans le cadre
          du module MA-24

# ------------------------------------------------------------------------------
# Revisions
# ------------------------------------------------------------------------------

# 2025-01-17 06 VCL
  - Version évaluation du 17.01.2025

# 2025-01-15 05 VCL
  - Simplification/nettoyage du code
    -> enlevé les fonctions bouge_gauche(), bouge_droite(),
       bouge_haut(), bouge_bas(), set_icon(), set_caption()
       ainsi que leur appel dans la fonction start()
    -> ajouté les fonctions dessine_pion(), nouveau_jeu()
       et fenetre_jeu()
    -> modifié la fonction plateau() au strict minimum (change
       juste la taille du plateau) et transféré le reste du code dans
       la nouvelle fonction fenetre_jeu()
    -> renomé des variables pour une meilleure lisibilité du code

# 2025-01-09 04 VCL
  - Ajouté la fonction selection()

  2024-12-05 03 PBA & VCL
  - Ajouté l'identification des événements de la souris avec la position

  2024-12-05 02 PBA & VCL
  - Ajouté les fonctions de déplacement haut, bas, gauche, droite
  - Changé le nom du fichier pion à charger

  2024-11-07 01 PBA & VCL
  - Version initiale qui fonctionne
"""

# Import de la librairie backend
import ma24_dames_rules as damesrules

# Import de la librairie graphique
import pygame


def _init():
    """Initilise la librairie gfx
    """
    global case_size, fichier_icone, screen, titre_jeu

    # Initialisation de pygame
    pygame.init()

    # Affiche l'icône et le titre de l'application
    icon = pygame.image.load(fichier_icone)
    pygame.display.set_icon(icon)

    # Affiche le titre de l'application
    pygame.display.set_caption(titre_jeu)

    # Initialisation de la fenêtre de jeu
    fenetre_jeu()

    damesrules.dessine_case = dessine_case
    damesrules.dessine_piece = dessine_piece
    damesrules.dessine_selection = dessine_selection


def fenetre_jeu():
    print("fenetre_jeu()")
    global nb_colonnes, nb_lignes, screen, COULEURS

    # Initialise le plateau de jeu
    damesrules.plateau((nb_colonnes, nb_lignes))

    # Crée la fenêtre graphique
    window_size = (case_size * nb_colonnes
                   + marge_gauche
                   + marge_droite,
                   case_size * nb_lignes
                   + marge_haut
                   + marge_bas
                   )
    screen = pygame.display.set_mode(window_size)

    # Ajoute le fond de la fenêtre graphique
    screen.fill(COULEURS["BACKGROUND"])


def plateau(taille_plateau=(10,10)):
    """Définit la taille du plateau en x (colonnes) y (lignes)
    """
    global nb_colonnes, nb_lignes

    # Garde en mémoire la taille du plateau
    nb_colonnes = taille_plateau[0]
    nb_lignes = taille_plateau[1]

    damesrules.plateau(taille_plateau)


def nouveau_jeu():
    """Initialise l'application pour une nouvelle partie
    """
    global nb_colonnes, nb_lignes
    damesrules.new_game()


def dessine_case(posx, posy, couleur):
    """Dessine la xème case du damier
    """
    global case_blanche, case_noire, case_size, marge_gauche, marge_haut,\
        screen

    case = case_blanche if couleur == damesrules.case_blanche else case_noire
    screen.blit(case, (marge_gauche + posx*case_size,
                       marge_haut + posy*case_size))
    pygame.display.flip()


def dessine_piece(posx, posy, piece):
    """Dessine la pièce sur le plateau
        piece définit si c'est un pion ou une dame
    """
    global case_size, dame_blanche, dame_noire, marge_gauche,\
        marge_haut, pion_blanc, pion_noir

    if piece//5:
        piece = dame_noire if piece % damesrules.blancs else dame_blanche
    else:
        piece = pion_noir if piece % damesrules.blancs else pion_blanc

    screen.blit(piece, (marge_gauche+posx*case_size,
                       marge_haut+posy*case_size))
    pygame.display.flip()


def dessine_selection(posx, posy, couleur):
    """Dessine le bord de la case selon la couleur passée en paramètre
    """
    global COULEURS, screen, marge_gauche, marge_haut, case_size
    pygame.draw.rect(screen, COULEURS[couleur],
        (marge_gauche + posx*case_size,
              marge_haut + posy*case_size,
              case_size,
              case_size),
              2)
    pygame.display.flip()


def selection(posx, posy):
    """Fonction appelée lors d'un click de souris
    """
    global marge_haut, marge_gauche, case_size
    case_x = (posx-marge_gauche) // case_size
    case_y = (posy-marge_haut) // case_size
    if damesrules.selectionable(case_x, case_y):
        pass


def start():
    """Démarre le jeu
    """
    running = True
    nouveau_jeu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Bouton de souris pressé")
                (bouton1, bouton2, bouton3) = pygame.mouse.get_pressed()
                (souris_x, souris_y) = pygame.mouse.get_pos()
                if bouton1:
                    print("-> bouton1 pressé (x :", souris_x, ", y : ", souris_y, ")")
                    selection(souris_x, souris_y)

                if bouton2:
                    print("-> bouton2 pressé (x :", souris_x, ", y : ", souris_y, ")")
                if bouton3:
                    print("-> bouton3 pressé (x :", souris_x, ", y : ", souris_y, ")")

            btn_presse = pygame.key.get_pressed()
            if btn_presse[pygame.K_RIGHT]:
                pass
            elif btn_presse[pygame.K_LEFT]:
                pass
            elif btn_presse[pygame.K_UP]:
                pass
            elif btn_presse[pygame.K_DOWN]:
                pass
            elif btn_presse[pygame.K_q]:
                running = False
    pygame.quit()

nb_colonnes = 10  # Nombre de cases horizontalement
nb_lignes = 10  # Nombre de cases verticalement
case_size = 80  # Taille des cases

# Couleurs
COULEURS = {
    "CASE BLANCHE" :(255, 255, 255),
    "CASE NOIRE" : (180, 180, 180),
    "BACKGROUND" : (89, 152, 255),
    "ENNEMI" : (255, 0, 0),
    "JOUEUR" : (0, 0, 255),
}

# Cases du damier
case_blanche = pygame.Surface((case_size, case_size))
case_blanche.fill(COULEURS["CASE BLANCHE"])
case_noire = pygame.Surface((case_size, case_size))
case_noire.fill(COULEURS["CASE NOIRE"])

# Marges autour du damier
marge_gauche = 10
marge_droite = 10
marge_haut = 10
marge_bas = 10

# Position actuelle du pion
pion_pos = [0, 0]  # positions en x, y

# Images à charger
chemin_images = "pictures\\"
fichier_icone = chemin_images + "International_draughts.png"
fichier_pion_blanc = chemin_images + "MA-24_pion_blanc.png"
fichier_dame_blanche = chemin_images + "MA-24_dame_blanche.png"
fichier_pion_noir = chemin_images + "MA-24_pion_noire.png"
fichier_dame_noire = chemin_images + "MA-24_dame_noire.png"

# Charge l'image du pion blanc
pion_blanc = pygame.image.load(fichier_pion_blanc)
pion_blanc = pygame.transform.scale(pion_blanc, (case_size, case_size))

# Charge l'image de la dame blanche
dame_blanche = pygame.image.load(fichier_dame_blanche)
dame_blanche = pygame.transform.scale(dame_blanche, (case_size, case_size))

# Charge l'image du pion blanc
pion_noir = pygame.image.load(fichier_pion_noir)
pion_noir = pygame.transform.scale(pion_noir, (case_size, case_size))

# Charge l'image de la dame noire
dame_noire = pygame.image.load(fichier_dame_noire)
dame_noire = pygame.transform.scale(dame_noire, (case_size, case_size))

# Titre du jeu
titre_jeu = "MA-24 : Jeu de Dames"
screen = pygame.Surface((0, 0))
_init()

print("module gfx loaded")