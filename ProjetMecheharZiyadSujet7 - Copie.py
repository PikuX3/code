#!/usr/bin/env python
# -*- coding: utf-8 -*-
#v1.2 : 
#    Eviter qu'un navire ne tire sur lui-même
#    Visualiser temporairement les tirs dans l'océan
#    Correction déplacement E6
#    Suppression des prints en commentaires
#v1.3 :
#    Renommer EstHorizontalNavire
#    Ennemi ne doit pas tirer depuis un navire est HS
#    Ennemi doit pouvoir continuer même si tous les navires allies sont HS
#v1.4 :
#    Vitesse differente pour chaque navire

#Modules importés
from tkinter import *
import random


"""
Projet : _______________
Auteur : _______________
Date de création : ______________
Description :__________
"""

# ----------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------

LARG_CASE=32#Largeur
HAUT_CASE=32#Hauteur


#Liste des navires alliés et ennemis
imNaviresAllies=[]
imNaviresEnnemis=[]
photosNaviresAllies=[]
photosNaviresEnnemis=[]
imDegats=[]
photosDegats=[]

#Etat de fonctionnement pour chaque navire
nbZonesOperationnellesNaviresAllies=[]
nbZonesOperationnellesNaviresEnnemis=[]

#Decor
imZonesOcean=[]
rectBaseAllies=[]
rectBaseEnnemis=[]
rectZonesIle=[]

#Menu choix de Navire
imChoixNavires=[]

typesDeplacement=["avancer","reculer","pivoter"]
directionsTir=["Nord","Sud","Est","Ouest"]

#Score
score=0
SCORE_NAVIRE_ENNEMI_ATTEINT=100
SCORE_NAVIRE_ALLIE_ATTEINT=-50
SCORE_BASE_ENNEMI_ATTEINTE=500
SCORE_BASE_ALLIE_ATTEINT=-100

#ModeArret=False;

#Cartographie
#OC = Zone Océan naviguable et disponible
#BA = Zone de la Base Alliée 
#BE = Zone de la Base Ennemie
#IL = Zone de l'ILe
#A2 = Zone occupée par le navire Allié de longueur 2
#E3 = Zone occupée par le navire Ennemi 3
#E3D = Zone occupée par le navire Ennemi 3 avec des dégats

matriceZones = [
    ["OC", "OC", "A5", "A5", "A5", "A5", "A5", "OC", "OC", "OC", "OC", "A2", "A2", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["BA", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["BA", "BA", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "A4", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["BA", "BA", "BA", "OC", "OC", "OC", "OC", "OC", "OC", "A4", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["BA", "BA", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "A4", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["BA", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "A4", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "E4", "E4", "E4", "E4", "OC"],
    ["A6", "A6", "A6", "A6", "A6", "A6", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "IL", "IL", "OC", "OC", "OC", "OC", "OC", "E2", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "IL", "IL", "IL", "IL", "OC", "OC", "OC", "OC", "E2", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "A3", "OC", "OC", "OC", "OC", "OC", "OC", "IL", "IL", "IL", "IL", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "A3", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "IL", "IL", "OC", "OC", "OC", "OC", "OC", "E6", "E6", "E6", "E6", "E6", "E6", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "A3", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "BE"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "E3", "OC", "OC", "OC", "OC", "BE", "BE"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "E3", "OC", "OC", "OC", "BE", "BE", "BE"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "E3", "OC", "OC", "OC", "OC", "BE", "BE"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "BE"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "E5", "E5", "E5", "E5", "E5", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"],
    ["OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC", "OC"]
]

#Dimensions
LARG_CANVAS = LARG_CASE*len(matriceZones[0])
HAUT_CANVAS = HAUT_CASE*len(matriceZones)

# ----------------------------------------------------------------
# Fonctions
# ----------------------------------------------------------------

"""
Obj: Gestion des évènements du clavier

"""
def evenements(event):

    if event.keysym=="Left":
        if EstHorizontalNavire(rbChoixNavire.get()):
            Deplacer(rbChoixNavire.get(),"reculer")
        else:
            Deplacer(rbChoixNavire.get(),"pivoter")
    elif event.keysym=="Right":
        if EstHorizontalNavire(rbChoixNavire.get()):
            Deplacer(rbChoixNavire.get(),"avancer")
        else:
            Deplacer(rbChoixNavire.get(),"pivoter")
    elif event.keysym=="Up":
        if EstHorizontalNavire(rbChoixNavire.get()):
            Deplacer(rbChoixNavire.get(),"pivoter")
        else:
            Deplacer(rbChoixNavire.get(),"avancer")
    elif event.keysym=="Down":
        if EstHorizontalNavire(rbChoixNavire.get()):
            Deplacer(rbChoixNavire.get(),"pivoter")
        else:
            Deplacer(rbChoixNavire.get(),"reculer")
    elif event.keysym=="z":
        Tir(rbChoixNavire.get(),"Nord")
    elif event.keysym=="s":
        Tir(rbChoixNavire.get(),"Sud")
    elif event.keysym=="q":
        Tir(rbChoixNavire.get(),"Ouest")
    elif event.keysym=="d":
        Tir(rbChoixNavire.get(),"Est")              
    #elif event.keysym=="Escape":#Touche Clavier Echap
    #elif event.keysym=="space"::#Touche Clavier espace
 

"""
Obj: Creation des Navires dnas le canvas
Paramètre NoNavire : correspondant à la longueur du Navire
Paramètre Camp : "Allie" ou "Ennemi"
"""
def CreationImagesNavire(NoNavire, Camp):
    global imNaviresAllies,photosNaviresAllies,photosNaviresEnnemis,imOC
    global nbZonesOperationnellesNaviresAllies,nbZonesOperationnellesNaviresEnnemis

    coordX=0
    coordY=0
    coordXPrecedent=-1
    nb=0
    #Identifiant Navire
    if (Camp=="Allie"):
        IdNavire="A"+str(NoNavire)
    else:
        IdNavire="E"+str(NoNavire)
        
    for i in range(len(matriceZones)):
        for j in range(len(matriceZones[i])):               
            if (matriceZones[i][j]==IdNavire):
                #Affichage de l'ocean
                nb=nb+1#Nombre de zones utilisées
                #Calcul des coordonnees de l'image
                coordX+=j*LARG_CASE
                coordY+=i*HAUT_CASE
                if (nb==2):#Calcul du sens de l'image
                    if ((j*LARG_CASE)==coordXPrecedent):
                        sens="Vertical"
                    else:
                        sens="Horizontal"
                coordXPrecedent=coordX
    #Affichage de l'image du navire dans le bon sens et aux bonnes coordonnees
    if (Camp=="Allie"):
        photosNaviresAllies.append(PhotoImage(file = "img/Navire "+Camp+" "+str(NoNavire)+" "+sens+".gif",master=fen_princ))
        imNaviresAllies.append(gestionCanvas.create_image(coordX/nb-(photosNaviresAllies[-1].width()/2)+LARG_CASE/2, 
                                                            coordY/nb+HAUT_CASE/2, 
                                                            image=photosNaviresAllies[-1],
                                                            anchor=W))
    else:
        photosNaviresEnnemis.append(PhotoImage(file = "img/Navire "+Camp+" "+str(NoNavire)+" "+sens+".gif",master=fen_princ))
        imNaviresEnnemis.append(gestionCanvas.create_image(coordX/nb-(photosNaviresEnnemis[-1].width()/2)+LARG_CASE/2, 
                                                            coordY/nb+HAUT_CASE/2, 
                                                            image=photosNaviresEnnemis[-1],
                                                            anchor=W))
    #Etat de fonctionnement initial (ou nombre de zones en état de fonctionnement) 
    #ex : Le navire A2 possède initialiement 2 zones en état de fcontionnement alors que 6 pour le E6
    if (Camp=="Allie"):
        nbZonesOperationnellesNaviresAllies.append(NoNavire)
    else:
        nbZonesOperationnellesNaviresEnnemis.append(NoNavire)

"""
Obj : Création et positionnement initial des images relatives aux bases alliés et ennemis ainsi que l'île'
"""
def CreationDecor():
    global imZonesOcean,rectBaseAllies,rectBaseEnnemis,rectZonesIle
   
    #Affichage de la base allié, ennemi, ainsi que l'ile
    for i in range(len(matriceZones)):
        for j in range(len(matriceZones[i])):
            if (matriceZones[i][j]=="BA"):
                rectBaseAllies.append(gestionCanvas.create_rectangle(j*LARG_CASE, i*HAUT_CASE,(j+1)*LARG_CASE, (i+1)*HAUT_CASE, fill="green"))
            elif (matriceZones[i][j]=="BE"):
                rectBaseEnnemis.append(gestionCanvas.create_rectangle(j*LARG_CASE, i*HAUT_CASE,(j+1)*LARG_CASE, (i+1)*HAUT_CASE, fill="red"))
            elif (matriceZones[i][j]=="IL"):
                rectZonesIle.append(gestionCanvas.create_rectangle(j*LARG_CASE, i*HAUT_CASE,(j+1)*LARG_CASE, (i+1)*HAUT_CASE, fill="yellow"))
            else:#(matriceZones[i][j]=="OC") ainsi que les zones occupees par les navires   
                imZonesOcean.append(gestionCanvas.create_image(j*LARG_CASE, i*HAUT_CASE, image=imOC,anchor=NW))
"""
Obj : 
Paramètre idNavire de type "A2" "E5"
"""
def EstHorizontalNavire(idNavire):
    ind=indexMinMaxNavire(idNavire)
    return ind[0][0]==ind[1][0]

"""
#Identification des coordonnees des 2 zones aux extremités du Navire en paramètre 
#Paramètre : idNavire : string de type A1, E5
#Sortie : [[iMin,jMin],[iMax,jMax]]
"""
def indexMinMaxNavire(idNavire):
    iMin=len(matriceZones)
    jMin=len(matriceZones[0])
    iMax=-1
    jMax=-1
    for i in range (len(matriceZones)):
        for j in range (len(matriceZones[i])):
            if (matriceZones[i][j].startswith(idNavire)):
                if (i>iMax):
                    iMax=i
                if (i<iMin):
                    iMin=i
                if (j>jMax):
                    jMax=j
                if (j<jMin):
                    jMin=j
    return [[iMin,jMin],[iMax,jMax]]

"""
#Mise à jour de la matrice d'un Navire suite à un déplacement ou un pivot
#Paramètres [iMin,jMin] et [iMax,jMax] : extremités du navire
#Paramètre delat : Rotation si delta =0 sinon translation de valeur delta zones 
"""
def MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,delta):
    global matriceZones

    if (iMin==iMax):#Horizontal
        if (delta>0):
            for j in range(jMax,jMin-1,-1):
                matriceZones[iMin][j+delta]=matriceZones[iMin][j]
                matriceZones[iMin][j]="OC"
        elif (delta<0):
            for j in range(jMin,jMax+1):
                matriceZones[iMin][j+delta]=matriceZones[iMin][j]
                matriceZones[iMin][j]="OC"
        else:#Rotation Vertical>Horizontal
            for k in range (1,jMax-jMin +1):
                matriceZones[iMin+k][jMin]=matriceZones[iMin][jMin+k]
                matriceZones[iMin][jMin+k]="OC"
    elif (jMin==jMax):#Vertical
        if (delta>0):
            for i in range(iMax,iMin-1,-1):
                matriceZones[i+delta][jMin]=matriceZones[i][jMin]
                matriceZones[i][jMin]="OC"
        elif (delta<0):
            for i in range(iMin,iMax+1):
                matriceZones[i+delta][jMin]=matriceZones[i][jMin]
                matriceZones[i][jMin]="OC"
        else:#Rotation Horizontal > Vertical
            for k in range (1,iMax-iMin +1):
                matriceZones[iMin][jMin+k]=matriceZones[iMin+k][jMin]
                matriceZones[iMin+k][jMin]="OC"


#Gestion du deplacement des navires 
#Paramètre : idNavire : string de type A1, E5
#Paramètre : "avancer" / "reculer" / "pivoter"
def Deplacer(idNavire, direction):
    
    global gestionCanvas,matriceZones,imNaviresAllies,photosNaviresAllies,imNaviresEnnemis,photosNaviresEnnemis
    
    
    #Identification du camp (Allies vs Ennemis)
    if (idNavire[0]=="A"):
        modeEnnemi=False
    else:#if (idNavire[0]=="E"):
        modeEnnemi=True
    
    
    #Identification du navire
    noNavire=int(idNavire[1])-2
    if (modeEnnemi==False):
        img=imNaviresAllies[noNavire]
    else:
        img=imNaviresEnnemis[noNavire]
        
    #Le navire doit être en état de fonctionnment pour se déplacer ou pivoter
    if ((modeEnnemi==True and nbZonesOperationnellesNaviresEnnemis[noNavire]>0) or 
        (modeEnnemi==False and nbZonesOperationnellesNaviresAllies[noNavire]>0)):
        
        #Vitesse différente des navires
        nbDeplacementsMax = (7-int(idNavire[1]));#A6 : Vitesse 1 / A5 : Vitesse 2...
        
        #Extrémités du navire
        ind=indexMinMaxNavire(idNavire)
        iMin=ind[0][0]
        jMin=ind[0][1]
        iMax=ind[1][0]
        jMax=ind[1][1]
        
        if (direction=="pivoter"):
            if jMin==jMax:#Vertical
                                
                #Disponibilité des zones avant la manoeuvre
                disponible=True
                for k in range (1,iMax-iMin +1):
                    if (jMin+k)>=len(matriceZones[iMin]) or matriceZones[iMin][jMin+k]!="OC":
                        disponible=False
                        break
                        
                #Si zones disponibles
                if (disponible==True):
                    MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,0)
                    if (modeEnnemi==False):
                        photosNaviresAllies[noNavire]=PhotoImage(file = "img/Navire Allie "+str(idNavire[1])+" Horizontal.gif",master=fen_princ)
                        gestionCanvas.itemconfig(img,image=photosNaviresAllies[noNavire])
                        gestionCanvas.move(img,0,-photosNaviresAllies[noNavire].width()*0.4)
                    else:
                        photosNaviresEnnemis[noNavire]=PhotoImage(file = "img/Navire Ennemi "+str(idNavire[1])+" Horizontal.gif",master=fen_princ)
                        gestionCanvas.itemconfig(img,image=photosNaviresEnnemis[noNavire])
                        gestionCanvas.move(img,0,-photosNaviresEnnemis[noNavire].width()*0.4)

            else:#Horizontal

                #Disponibilité des zones avant la manoeuvre
                disponible=True
                for k in range (1,jMax-jMin +1):
                    if (iMin+k)>=len(matriceZones) or matriceZones[iMin+k][jMin]!="OC":
                        disponible=False
                        break
                        
                #Si zones disponibles
                if (disponible==True):
                    MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,0)
                    if (modeEnnemi==False):
                        photosNaviresAllies[noNavire]=PhotoImage(file = "img/Navire Allie "+str(idNavire[1])+" Vertical.gif",master=fen_princ)
                        gestionCanvas.itemconfig(img,image=photosNaviresAllies[noNavire])
                        gestionCanvas.move(img,0,photosNaviresAllies[noNavire].height()*0.4)
                    else:
                        photosNaviresEnnemis[noNavire]=PhotoImage(file = "img/Navire Ennemi "+str(idNavire[1])+" Vertical.gif",master=fen_princ)
                        gestionCanvas.itemconfig(img,image=photosNaviresEnnemis[noNavire])
                        gestionCanvas.move(img,0,photosNaviresEnnemis[noNavire].height()*0.4)

        else :
        
            nbDeplacements=0
            collision=False
            while (collision==False and nbDeplacements<nbDeplacementsMax):
                #Mise à jour des extrémités du navire
                ind=indexMinMaxNavire(idNavire)
                iMin=ind[0][0]
                jMin=ind[0][1]
                iMax=ind[1][0]
                jMax=ind[1][1]
                
                #Tester si destination et trajet disponible dans la Matrice
                if jMin==jMax:#Vertical
                    if (direction=="avancer"):
                        if (iMin>0 and matriceZones[iMin-1][jMin]=="OC"):
                            nbDeplacements=nbDeplacements+1
                            MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,-1)
                            gestionCanvas.move(img, 0, -HAUT_CASE)
                        else:
                            collision=True
                    elif (direction=="reculer"):
                        if (iMax<(len(matriceZones)-1) and matriceZones[iMax+1][jMin]=="OC"):
                            nbDeplacements=nbDeplacements+1
                            MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,1)
                            gestionCanvas.move(img, 0, HAUT_CASE)
                        else:
                            collision=True
    
                    
                else:#Horizontal
                    if (direction=="avancer"):
                        if (jMax<(len(matriceZones[iMax])-1) and matriceZones[iMax][jMax+1]=="OC"):
                            nbDeplacements=nbDeplacements+1
                            MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,1)
                            gestionCanvas.move(img, LARG_CASE, 0)
                        else:
                            collision=True
                    elif (direction=="reculer"):
                        if ((jMin>0) and matriceZones[iMin][jMin-1]=="OC"):
                            nbDeplacements=nbDeplacements+1
                            MiseAJourMatrice_PositionNavire(iMin,iMax,jMin,jMax,-1)
                            gestionCanvas.move(img, -LARG_CASE, 0)
                        else:
                            collision=True
        #Fin du déplacement
        ActualiserPositionsZonesDegats()
    if (modeEnnemi==False):
        ActionEnnemi()
        
        lblTitreInfo.config(text="Deplacer ")
        lblInfo.config(text=(idNavire, direction))
"""
Obj : Après un déplacement ou un tir Allié, les ennemis attaquent ou se déplacent à leur tour
"""
def ActionEnnemi():
    if (random.randint(0, 1)==0):
        Deplacer("E"+str(random.randint(2, 6)), typesDeplacement[random.randint(0, 2)])
    else:
        Tir("E"+str(random.randint(2, 6)), directionsTir[random.randint(0, 3)])
            
"""
Obj : Réorganisation des images de dégats afin d'assurer une position cohérente
"""
def ActualiserPositionsZonesDegats():
    global matriceZones,imDegats
    
    #Effacer les dégats
    for i in range(len(imDegats)):
        gestionCanvas.delete(photosDegats[i])
        gestionCanvas.delete(imDegats[i])
    photosDegats.clear()
    imDegats.clear()
    
    for i in range(len(matriceZones)):
        for j in range(len(matriceZones[i])):
            if (len(matriceZones[i][j])>2 and matriceZones[i][j][2]=="D"):
                photosDegats.append(PhotoImage(file = "img/touche.gif",master=fen_princ))
                imDegats.append(gestionCanvas.create_image(j*LARG_CASE-(photosDegats[-1].width()/2)+LARG_CASE/2, 
                                                                    i*LARG_CASE+HAUT_CASE/2, 
                                                                    image=photosDegats[-1],
                                                                    anchor=W))

"""
#Obj : Gestion des tirs
#Paramètre : idNavire : string de type A1, E5
#Paramètre : direction : "Nord" "Sud" "Est" ou "Ouest"
"""
def Tir(idNavire, direction):
    global matriceZones,imDegats,score,lblScore,lblInfo

    
    #Actualiser les dégats
    if (idNavire[0]=="A"):
        ActualiserPositionsZonesDegats()

    #Identification du camp (Allies vs Ennemis)
    if (idNavire[0]=="A"):
        modeEnnemi=False
    else:#if (idNavire[0]=="E"):
        modeEnnemi=True
    
    #Identification du navire
    noNavire=int(idNavire[1])-2
    
    #Le navire doit être en état de fonctionnment pour tirer
    if ((modeEnnemi==True and nbZonesOperationnellesNaviresEnnemis[noNavire]>0) or 
        (modeEnnemi==False and nbZonesOperationnellesNaviresAllies[noNavire]>0)):
        
    
        #Portee différente des navires
        PorteeMax = int(idNavire[1]);#A6 : Portée de 6 / A5 : Portée de 5 zones...
        
        #Extrémités du navire
        ind=indexMinMaxNavire(idNavire)
        iMin=ind[0][0]
        jMin=ind[0][1]
        iMax=ind[1][0]
        jMax=ind[1][1]
        
        #Coordonnées du tir prenant en compte la direction et la portée du navire
        if (direction=="Nord"):
            iCible=iMin-random.randint(1, PorteeMax)
            jCible=random.randint(jMin-1,jMax+1)
        elif (direction=="Sud"):
            iCible=iMax+random.randint(1, PorteeMax)
            jCible=random.randint(jMin-1,jMax+1)
        elif (direction=="Ouest"):
            iCible=random.randint(iMin-1,iMax+1)
            jCible=jMin-random.randint(1, PorteeMax)
        elif (direction=="Est"):
            iCible=random.randint(iMin-1,iMax+1)
            jCible=jMax+random.randint(1, PorteeMax)
        
        if (iCible<0 or iCible>=len(matriceZones) or jCible<0 or jCible>=len(matriceZones[iCible])):
            print("Hors zone")
        elif (len(matriceZones[iCible][jCible])<3):
            #Présence d'un troisième caractère uniquement pour les zones déjà endommagées
            
            #Afficher image impact
            photosDegats.append(PhotoImage(file = "img/touche.gif",master=fen_princ))
            imDegats.append(gestionCanvas.create_image(jCible*LARG_CASE-(photosDegats[-1].width()/2)+LARG_CASE/2, 
                                                                iCible*LARG_CASE+HAUT_CASE/2, 
                                                                image=photosDegats[-1],
                                                                anchor=W))
            #Sauvegarder les conséquences de ce tir
            if (not matriceZones[iCible][jCible].startswith("OC")):
                #Mise à jour de la matrice
                matriceZones[iCible][jCible]=matriceZones[iCible][jCible][0:2]+"D"
                #?Mise à jour de l'état de fonctionnement
                if matriceZones[iCible][jCible].startswith("A"):
                    iNavireTouche=int(matriceZones[iCible][jCible][1])-2
                    nbZonesOperationnellesNaviresAllies[iNavireTouche]=nbZonesOperationnellesNaviresAllies[iNavireTouche]-1
                elif matriceZones[iCible][jCible].startswith("E"):    
                    iNavireTouche=int(matriceZones[iCible][jCible][1])-2
                    nbZonesOperationnellesNaviresEnnemis[iNavireTouche]=nbZonesOperationnellesNaviresEnnemis[iNavireTouche]-1
            
            #Gestion du score
            if (matriceZones[iCible][jCible].startswith("A")):
                score=score+SCORE_NAVIRE_ALLIE_ATTEINT
            elif (matriceZones[iCible][jCible].startswith("E")):
                score=score+SCORE_NAVIRE_ENNEMI_ATTEINT
            elif (matriceZones[iCible][jCible].startswith("BA")):
                score=score+SCORE_BASE_ALLIE_ATTEINT
            elif (matriceZones[iCible][jCible].startswith("BE")):
                score=score+SCORE_BASE_ENNEMI_ATTEINTE
    #Fin du Tir
    if (modeEnnemi==False):
        ActionEnnemi()
    lblTitreInfo.config(text="Tir")     
    lblInfo.config(text=(idNavire, direction))
    #Vérifier et annoncer si la partie est terminée
    lblScore.config(text=str(score))
    if (victoireAllies()):
        lblTitreScore.config(text="Victoire !")
    elif (victoireEnnemis()):
        lblTitreScore.config(text="Defaite !")

   

"""
Obj : Retourne Vrai si les Alliés ont gagnés
"""
def victoireAllies():
    nbZonesSainesBaseEnnemi=0
    for i in range(0,len(matriceZones)):
        for j in range(0,len(matriceZones[i])):
            if (matriceZones[i][j].startswith("BE") and matriceZones[i][j]!="BED"):
                nbZonesSainesBaseEnnemi=nbZonesSainesBaseEnnemi+1
                
    return (nbZonesSainesBaseEnnemi==0)

"""
obj : Retourne Vrai si les Ennemis ont gagné 
"""
def victoireEnnemis():
    nbZonesSainesBaseAllie=0
    for i in range(0,len(matriceZones)):
        for j in range(0,len(matriceZones[i])):
            if (matriceZones[i][j].startswith("BA") and matriceZones[i][j]!="BAD"):
                nbZonesSainesBaseAllie=nbZonesSainesBaseAllie+1
                
    return (nbZonesSainesBaseAllie==0)

# ----------------------------------------------------------------
# Corps du programme
# ----------------------------------------------------------------

#Paramétrage de la fenêtre principale
fen_princ = Tk()
fen_princ.title("Sea battle L1 SPI 2022-2023")
fen_princ.geometry(str(LARG_CANVAS+300)+"x"+str(HAUT_CANVAS+100))#Dimensions de la fenêtre
fen_princ.bind("<Key>",evenements)#Définition de la fonction de gestion des évènements clavier

#Paramétrage du Canvas
gestionCanvas = Canvas(fen_princ, width=LARG_CANVAS, height=HAUT_CANVAS, bg='ivory', bd=0, highlightthickness=0)
gestionCanvas.grid(row=0,column=0, padx=10,pady=10)

#Images pour ocean, bases, ile
imOC = PhotoImage(file = 'img/Ocean_small.gif', master=fen_princ)
CreationDecor()

#Images des navires stockées dans la liste imNaviresAllies
#imNaviresAllies[0] = Navire A2 / [1]=A3 / [2]=A4 / [3]=A5 / [4]=A6
for i in range(2,7):
    CreationImagesNavire(i,"Allie")
    
#Images des navires stockées dans la liste imNaviresEnnemis
#imNaviresEnnemis[0] => Navire E2 / [1]=E3 / [2]=E4 / [3]=E5 / [4]=E6
for i in range(2,7):
    CreationImagesNavire(i,"Ennemi") 
    
    
#Zone dédiée aux boutons
zoneBtn = Frame(fen_princ)
zoneBtn.grid(row=0,column=1,ipadx=5)


lblTitreInfo = Label(zoneBtn,text="\n= Info =\n")
lblTitreInfo.pack(fill=X)

lblTitreInfo = Label(zoneBtn,text="  ")
lblTitreInfo.pack(fill=X)
lblInfo = Label(zoneBtn,text="0")
lblInfo.pack(fill=X)

#Score
lblTitreScore = Label(zoneBtn,text="\n= Score =\n")
lblTitreScore.pack(fill=X)
lblScore = Label(zoneBtn,text="0")
lblScore.pack(fill=X)

lblVictoire = Label(zoneBtn,text="")
lblVictoire.pack(fill=X)


#Choix du navire
lblChoixNavire = Label(zoneBtn,text="\n= Choix Navire =\n")
lblChoixNavire.pack()

valsNavires = ['A2', 'A3', 'A4','A5','A6']
rbChoixNavire = StringVar()
rbChoixNavire.set(valsNavires[0])#Valeurs par defaut

for i in range(len(valsNavires)):
    imChoixNavires.append(PhotoImage(file="img/Navire Allie "+valsNavires[i][1]+" Horizontal.gif"))
    rbNavire = Radiobutton(zoneBtn, variable=rbChoixNavire, value=valsNavires[i], indicatoron=0,image=imChoixNavires[i])
    rbNavire.pack(side='top', expand=1)

#Boutons directionnels
lblChoixDirection = Label(zoneBtn,text="\n= Choix Navigation =\n")
lblChoixDirection.pack()


btnAvancer = Button(zoneBtn, text="Avancer", fg="cyan", bg="black", command=lambda:Deplacer(rbChoixNavire.get(),"avancer"))
btnAvancer.pack(fill=X)

btnReculer = Button(zoneBtn, text="Reculer", fg="cyan", bg="black", command=lambda:Deplacer(rbChoixNavire.get(),"reculer"))
btnReculer.pack(fill=X)

btnPivoter = Button(zoneBtn, text="Pivoter", fg="cyan", bg="black", command=lambda:Deplacer(rbChoixNavire.get(),"pivoter"))
btnPivoter.pack(fill=X)


lblChoixAction = Label(zoneBtn,text="\n= Choix Action =\n")
lblChoixAction.pack()

btnTirAvant = Button(zoneBtn, text="TIR Nord", fg="black", bg="red", command=lambda:Tir(rbChoixNavire.get(),"Nord"))
btnTirAvant.pack(fill=X)
btnTirArriere = Button(zoneBtn, text="TIR Sud", fg="black", bg="red", command=lambda:Tir(rbChoixNavire.get(),"Sud"))
btnTirArriere.pack(fill=X)
btnTirGauche = Button(zoneBtn, text="TIR Ouest", fg="black", bg="red", command=lambda:Tir(rbChoixNavire.get(),"Ouest"))
btnTirGauche.pack(fill=X)
btnTirDroite = Button(zoneBtn, text="TIR Est", fg="black", bg="red", command=lambda:Tir(rbChoixNavire.get(),"Est"))
btnTirDroite.pack(fill=X)

# Initialiser les images pour les navires ennemis
for i in range(3):
    imNaviresEnnemis.append(PhotoImage(file="navire_ennemi.gif"))
    # Les navires ennemis sont initialement invisibles
    imNaviresEnnemis[i].visible = False
    photosNaviresEnnemis.append(canvas.create_image(x, y, image=imNaviresEnnemis[i], anchor=CENTER))
# Si un navire ennemi est touché par un projectile
if navire_enemi_touche:
    # Rendre le navire ennemi visible
    imNaviresEnnemis[index_navire_touche].visible = True
else:
    # Rendre tous les navires ennemis invisibles
    for i in range(len(imNaviresEnnemis)):
        imNaviresEnnemis[i].visible = False


