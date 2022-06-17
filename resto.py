from ast import arg
import multiprocessing as mp
import random as rand 
import time


# ------------------ Client ------------------
def client_program(orderQueue, messageQueue, lockSendMessage):
    commandes_dispo = ['Big Mac', 'Triple Cheese Burger', 'Sundae', 'CBO']
    while True:   
        randomCommandeIndex = rand.randint(0,len(commandes_dispo)-1)
        commande = commandes_dispo[randomCommandeIndex]
        orderQueue.put(commande)
        with lockSendMessage:
            messageQueue.put('La commande "' + commande + '" vient d\'être lancée !')
        #Attente de x secondes avant de lancer une nouvelle commande
        time.sleep(rand.randint(1,3))


    
# ------------------ Major d'Homme ------------------
def majordhomme_program(messageQueue):
    while True:
        message = messageQueue.get()
        print(message)



# ------------------ Serveur ------------------
def server_program(i,orderQueue, messageQueue,lockPickOrderInQueue,lockSendMessage):
    while True:
        with lockPickOrderInQueue: #un seul serveur prend une commande dans la file à la fois.
            commande = orderQueue.get()
        with lockSendMessage:
            messageQueue.put("Le serveur n°" + str(i) + " s'occupe de la commande: " + str(commande) + " !") 
        time.sleep(rand.randint(1,10))
        with lockSendMessage:
            messageQueue.put("La commande " + str(commande) + " a été traitée par le serveur n°" + str(i) + " !" )
            
class ServersManager:
    def __init__(self, nb_servers,programToRun,orderQueue, messageQueue,lockPickOrderInQueue,lockSendMessage):

        self.nb_servers = nb_servers
        self.servers = self.createNServer(programToRun,orderQueue, messageQueue,lockPickOrderInQueue,lockSendMessage)
        

    
    def createNServer(self,programToRun,orderQueue, messageQueue,lockPickOrderInQueue,lockSendMessage):
        servers = []
        if self.nb_servers > 0:
            for i in range(self.nb_servers):
                servers.append(mp.Process(target=programToRun, args=(i,orderQueue,messageQueue,lockPickOrderInQueue,lockSendMessage))) 
            return servers
        else:
            print('Le nombre de serveur est incorrect')

    def start(self):
        for server in self.servers:
            server.start()
    def join(self):
        for server in self.servers:
            server.join()




if __name__ == '__main__':

    #Création de la fin d'attente des commandes 
    orderQueue = mp.Queue()

    #Création de la fin d'attente des messages affiché par le major d'homme
    messageQueue = mp.Queue()

    #Création des verrous de modification de la file d'attente de commande et d'envoi es messages des serveurs au major d'homme
    lockPickOrderInQueue = mp.Lock()
    lockSendMessage = mp.Lock()


    #Création du client
    client = mp.Process(target=client_program, args=(orderQueue,messageQueue, lockSendMessage))

    #Création des serveurs
    n = 5 #nombre de serveurs
    gestionnaireDesServeurs = ServersManager(n,server_program,orderQueue, messageQueue,lockPickOrderInQueue,lockSendMessage)

    #Création du major d'homme
    majorDHomme = mp.Process(target=majordhomme_program , args=(messageQueue,))


    #On demarre tous les processus !
    client.start()
    gestionnaireDesServeurs.start()
    majorDHomme.start()
    

    client.join()
    gestionnaireDesServeurs.join()
    majorDHomme.join()
    




 
    




