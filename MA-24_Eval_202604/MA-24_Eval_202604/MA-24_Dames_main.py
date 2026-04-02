#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Name    : MA-24_Dames_main.py
Authors : Attivon Kodjo
Date    : 2024.12.05
Version : 0.02
Purpose : Jeu de dames avec la librairie pygame

# ------------------------------------------------------------------------------
# Revisions
# ------------------------------------------------------------------------------

# 2024-12-05 02 PBA & VCL
  - Changé l'affichage dans la console de l'information concernant la
    taille du plateau

  2024-11-07 01 PBA & VCL
  - Version initiale
"""

import ma24_dames_gfx as damesgfx


# ------------
# --- MAIN ---
# ------------

#Définition des constantes
taille_plateau = (10, 9)
damesgfx.plateau(taille_plateau)
print ("Plateau de", taille_plateau[0], "par", taille_plateau[1])
damesgfx.start()
