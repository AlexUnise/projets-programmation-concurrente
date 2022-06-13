from ast import arg
import multiprocessing as mp
import random as rand 
import time

def createNServer(n,program,bufferCmde, verrouCmde):
        if n > 0:
            server_list = []
            for i in range(n):
                server_list.append(mp.Process(target=program, args=(i,bufferCmde,verrouCmde)))
            for server in server_list:
                server.start()
        else:
            print('Le nombre de serveur est incorrect')


# ------------------ Client ------------------
def client_program (bufferCmde, verrouCmde):
    while True:

        
        commandes_dispo = ['Big Mac', 'Triple Cheese Burger', 'Sundae', 'CBO']

        randomCommandeIndex = rand.randint(0,len(commandes_dispo)-1)
        print(commandes_dispo[randomCommandeIndex])









        #Attente de n secondes avant une nouvelle commande 
        time.sleep(rand.randint(1,3))

# ------------------ Serveur ------------------
def serveur_program(idServeur,bufferCmde, verrouCmde):
    pass


# ------------------ Major d'Homme ------------------
def majordhomme_program (bufferCmde,verrouCmde,  ):
    pass



    

    




if __name__ == '__main__':
    #Création du tampon de commandes
    bufferCmde = mp.Manager().list()
    verrouCmde = mp.Lock()
    
    
    s = 5
    client = mp.Process(target=client_program, args=(bufferCmde,verrouCmde))
    client.start()

    createNServer(s,bufferCmde,verrouCmde) #créer et start les serveurs

    majorDhomme = mp.Process(target=majordhomme_program, args=(bufferCmde, verrouCmde))
    




