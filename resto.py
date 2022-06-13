from ast import arg
import multiprocessing as mp
import random as rand 
import time

def createNServer(n,program,bufferCmde,etat_serveurs, serveur_pointeur, verrouCmde,isNewOrder, isCooking, hasDoneCoking):
        if n > 0:
            server_list = []
            for i in range(n):
                server_list.append(mp.Process(target=program, args=(i,bufferCmde,etat_serveurs,serveur_pointeur, verrouCmde,isNewOrder, isCooking, hasDoneCoking)))
            for server in server_list:
                server.start()
            return server_list
        else:
            print('Le nombre de serveur est incorrect')
        


# ------------------ Client ------------------
def client_program (bufferCmde, verrouCmde):
    while True:

        
        commandes_dispo = ['Big Mac', 'Triple Cheese Burger', 'Sundae', 'CBO']
        randomCommandeIndex = rand.randint(0,len(commandes_dispo)-1)
        bufferCmde.append(commandes_dispo[randomCommandeIndex])
        isNewOrder.set()








        #Attente de n secondes avant une nouvelle commande 
        time.sleep(rand.randint(1,3))

# ------------------ Serveur ------------------
def serveur_program(idServeur,bufferCmde,etat_serveurs, serveur_pointeur, verrouCmde,isNewOrder, isCooking, hasDoneCoking):

    hasCommande = False

    while True:
        if isNewOrder and not hasCommande:
            with verrouCmde:
                hasCommande = True
                with verrouEtatServeurs:
                    etat_serveurs[idServeur]['commande'] = bufferCmde.pop(-1)
                    with verrouServeurPointeur:
                        serveur_pointeur.value = idServeur
                        isCooking.set()
            time.sleep(rand.randint(1,10))
            isCooking.clear()
            with verrouServeurPointeur:
                serveur_pointeur.value = idServeur
                hasDoneCoking.set()
                hasCommande = False
                etat_serveurs[idServeur]['commande'] = None


    


# ------------------ Major d'Homme ------------------
def majordhomme_program (bufferCmde, etat_serveurs,serveur_pointeur, verrouCmde,isCooking, hasDoneCoking):
    if isCooking.is_set():
        with verrouEtatServeurs:
            with verrouServeurPointeur:
                serveurID = serveur_pointeur.value
                print('Le serveur ', etat_serveurs[serveurID]["id"], " traite la commande ", etat_serveurs[serveurID]["commande"])
    if hasDoneCoking.is_set():
        with verrouServeurPointeur:
                serveurID = serveur_pointeur.value
                print("Commande ",  etat_serveurs[serveurID]["commande"]  ,"est servie au client")



    

    




if __name__ == '__main__':
    #Création du tampon de commandes
    bufferCmde = mp.Manager().list()
    verrouCmde = mp.Lock()

    #Evenements
    isNewOrder = mp.Manager().Event()
    isCooking = mp.Manager().Event()
    hasDoneCoking = mp.Manager().Event()

    #Liste d'état des serveurs
    etat_serveurs= mp.Manager().list()
    verrouEtatServeurs = mp.Lock()
    
    #Pointeur de serveur
    serveur_pointeur = mp.Value('i', 0)
    verrouServeurPointeur = mp.Lock()

    
    s = 5

    client = mp.Process(target=client_program, args=(bufferCmde,verrouCmde))
    client.start()

    
    etat_serveurs = [{"id": x, "command": None} for x in range(s)]
    serveurs = createNServer(s,serveur_program,bufferCmde, etat_serveurs, serveur_pointeur, verrouCmde, isNewOrder, isCooking, hasDoneCoking) #créer et start les serveurs


    majorDhomme = mp.Process(target=majordhomme_program, args=(bufferCmde, etat_serveurs, serveur_pointeur, verrouCmde, isCooking, hasDoneCoking))
    majorDhomme.start()
    




