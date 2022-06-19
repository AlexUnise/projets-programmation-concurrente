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



#fonction qui initialise la matrice display avec de cellules vivantes ou mortes
def DisplaySetup(width,height):
    Display=[]

    for i in range(height):
        liste_UserLigne=[]
        for j in range(width):
            die=random.randint(1,6)
            if die >3:
                liste_UserLigne.append(0)
            else:
                liste_UserLigne.append(1)
        Display.append(liste_UserLigne)
    return Display



#fonction qui va couper en 4 matrices la matrice display
def DivideDisplay(nb_proc,Display):
    DividedDisplay=[[] for i in range(nb_proc)]
    for indl,ligne in enumerate(Display):
        liste1=[]
        liste2=[]
        liste3=[]
        liste4=[]
        for indc,cell in enumerate(ligne):
            if indl<len(Display)/2:
                if indc<len(Display[0])/2:
                    liste1.append(cell)
                else:
                    liste2.append(cell)
            else:
                if indc<len(Display[0])/2:
                    liste3.append(cell)
                else:
                    liste4.append(cell)
        if len(liste1)!=0:
            DividedDisplay[0].append(liste1)
        if len(liste2)!=0:
            DividedDisplay[1].append(liste2)
        if len(liste3)!=0:
            DividedDisplay[2].append(liste3)
        if len(liste4)!=0:
            DividedDisplay[3].append(liste4)
    return DividedDisplay


#La fonction qui va etre utilisee par les processus, elle traite 1/4 de la matrice display
def UpdateUserDisplay(Display,FutureDisplay,DivDisplay,i,VerrouDisp):
    for indl,ligne in enumerate(DivDisplay):
        for indc,cell in enumerate(ligne):
            neighbours,x,y=get_neighbours(Display,indl,indc,i)
            update_cell(Display,FutureDisplay,neighbours,x,y,VerrouDisp)
            position=15
            with VerrouDisp:
                curseur_invisible()
                move_to(position+x, y)
                en_couleur(lyst_colors[FutureDisplay[x*len(Display[0])+y]+1])
                print(FutureDisplay[x*len(Display[0])+y])
                
    move_to(position+5, 1)

    sys.exit(0)
    

    
#Cette fonction va mettre a jour une cellule donnee en fonction de ses voisins
def update_cell(Display,FutureDisplay,neighbours,indl,indc,VerrouDisp):
    live_cells=0
    for cell in neighbours:
        if int(cell)==1:
            live_cells+=1

    if Display[indl][indc]==1:
        if live_cells<2:
            with VerrouDisp:
                FutureDisplay[indl*len(Display[0])+indc]=0
        elif live_cells>3:
            with VerrouDisp:
                FutureDisplay[indl*len(Display[0])+indc]=0
            
    else:
        if live_cells==3:
            with VerrouDisp:
                FutureDisplay[indl*len(Display[0])+indc]=1




#Cette fonction va chercher tous les voisins pour une cellule donnee
def get_neighbours(Display,indl,indc,i):
    if i==1:
        indc+=int(len(Display[0])/2)
    elif i==2:
        indl+=int(len(Display)/2)
    elif i==3:
        indl+=int(len(Display)/2)
        indc+=int(len(Display[0])/2)
    neighbours=[]
    try:    
        if indl-1>0 and indc-1>0:
            neighbours.append(Display[indl-1][indc-1])
    except IndexError:
        None
    try:    
        if indl-1>0:
            neighbours.append(Display[indl-1][indc])
    except IndexError:
        None
    try:    
        if indl-1>0:
            neighbours.append(Display[indl-1][indc+1])
    except IndexError:
        None
    try:
        if indc-1>0:    
            neighbours.append(Display[indl][indc-1])
    except IndexError:
        None
    try:    
        neighbours.append(Display[indl][indc+1])
    except IndexError:
        None
    try:    
        if indc-1>0:
            neighbours.append(Display[indl+1][indc-1])
    except IndexError:
        None
    try:    
        neighbours.append(Display[indl+1][indc])
    except IndexError:
        None
    try:    
        neighbours.append(Display[indl+1][indc+1])
    except IndexError:
        None
    
    return neighbours,indl,indc


#Programme principal qui va permettre de lancer les 4 processus
if __name__ == "__main__":
    Nb_process=4
    Display=DisplaySetup(20,20)
    FutureDisplay=mp.Array('i',[0 for i in range(len(Display)*len(Display[0]))])
    mes_process = [0 for i in range(Nb_process)]
    VerrouDisp=mp.Lock()
    
    while True:
        time.sleep(0.1)
        DividedDisplay=DivideDisplay(Nb_process,Display)#On divise en 4 matrices pour nos 4 processus
        for i in range(Nb_process): # Lancer Nb_process processus
            
            mes_process[i] = mp.Process(target=UpdateUserDisplay, args=(Display,FutureDisplay,DividedDisplay[i],i,VerrouDisp,))
            mes_process[i].start()
        for i in range(Nb_process): mes_process[i].join()
        for i,line in enumerate(Display):
            for j,cell in enumerate(line):
                Display[i][j]=FutureDisplay[i*len(Display[0])+j]# On actualise notre matrice Display
        


        