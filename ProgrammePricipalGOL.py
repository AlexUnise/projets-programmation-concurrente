import os,sys,time,random
import multiprocessing as mp



CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEAREOS = "\x1B[J" # Clear End Of Screen
CLEARELN = "\x1B[2K" # Clear Entire LiNe
CLEARCUP = "\x1B[1J" # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH" # ('H' ou 'f') : Goto at (y,x), voir le code
DELAFCURSOR = "\x1B[K" # effacer après la position du curseur
CRLF = "\r\n" # Retour à la ligne
# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h" # Curseur visible
CURSOFF = "\x1B[?25l" # Curseur invisible
# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m" # Normal
BOLD = "\x1B[1m" # Gras
UNDERLINE = "\x1B[4m" # Souligné
# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m" # Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m" # Rouge
CL_GREEN="\033[22;32m" # Vert
CL_BROWN = "\033[22;33m" # Brun
CL_BLUE="\033[22;34m" # Bleu
CL_MAGENTA="\033[22;35m" # Magenta
CL_CYAN="\033[22;36m" # Cyan
CL_GRAY="\033[22;37m" # Gris
# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m" # Gris foncé
CL_LIGHTRED="\033[01;31m" # Rouge clair
CL_LIGHTGREEN="\033[01;32m" # Vert clair
CL_YELLOW="\033[01;33m" # Jaune
CL_LIGHTBLU= "\033[01;34m" # Bleu clair
CL_LIGHTMAGENTA="\033[01;35m" # Magenta clair
CL_LIGHTCYAN="\033[01;36m" # Cyan clair
CL_WHITE="\033[01;37m" # Blanc
#−−−−−−−−with verrou_print:−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
import multiprocessing as mp
import numpy as np
import os, time,math, random, sys, ctypes

# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')
def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !

class GameOfLife():
    def __init__(self,DisplayHeight,DisplayWidth):
        self.__DisplayHeight = DisplayHeight
        self.__DisplayWidth = DisplayWidth
        self.__UserDisplay=[]
        self.__Display = []
        self.__verrou_print=mp.Lock()

    def DisplaySetup(self):

        for i in range(self.__DisplayHeight):
            liste_ligne=[]
            liste_UserLigne=[]
            for j in range(self.__DisplayWidth):
                die=random.randint(1,6)
                if die >1:
                    liste_ligne.append(Cell(False))
                    liste_UserLigne.append(".")
                else:
                    liste_ligne.append(Cell(True))
                    liste_UserLigne.append("0")
            self.__Display.append(liste_ligne)
            self.__UserDisplay.append(liste_UserLigne)

    def UpdateDisplay(self):
        effacer_ecran()
        curseur_invisible()
        position=5
        for i in self.__UserDisplay:
            with self.__verrou_print:
                    move_to(position, 1)
                    erase_line_from_beg_to_curs()
                    en_couleur(lyst_colors[2])
                    print("".join(i))
            position+=1
        move_to(position+5, 1)

    def UpdateUserDisplay(self,cell,indl,indc):
        if cell.get_state() ==True:
            self.__UserDisplay[indl][indc]="0"
        else:
            self.__UserDisplay[indl][indc]="."

    def get_neighbours(self,indl,indc):
        neighbours=[]
        try:    
            neighbours.append(self.__Display[indl-1][indc-1])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl-1][indc])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl-1][indc+1])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl][indc-1])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl][indc+1])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl+1][indc-1])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl+1][indc])
        except IndexError:
            None
        try:    
            neighbours.append(self.__Display[indl+1][indc+1])
        except IndexError:
            None
        
        
        return neighbours

    def UpdateGame(self):
        for indl,ligne in enumerate(self.__Display):
            for indc,cell in enumerate(ligne):
                cell.update_cell(self.get_neighbours(indl,indc))
        for indl,ligne in enumerate(self.__Display):
            for indc,cell in enumerate(ligne):
                cell.actualise_state()
                self.UpdateUserDisplay(cell,indl,indc)
        self.UpdateDisplay()        

class Cell():
    def __init__(self,state):
        self.__alive=state
        self.__future=state

    def kill_cell(self):
        self.__future=False
    def spawn_cell(self):
        self.__future=True
    def get_state(self):
        return self.__alive

    def actualise_state(self):
        self.__alive=self.__future

    def update_cell(self,neighbours):
        live_cells=0
        for cell in neighbours:
            if cell.get_state()==True:
                live_cells+=1
        if self.__alive==True:
            if live_cells<2:
                self.kill_cell()
            elif live_cells>3:
                self.kill_cell()
                
        else:
            if live_cells==3:
                self.spawn_cell()



game=GameOfLife(30,50)
game.DisplaySetup()


while True:
    game.UpdateGame()
    time.sleep(0.1)
    