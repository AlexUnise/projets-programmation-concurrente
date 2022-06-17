from ast import arg
import multiprocessing as mp
import random as rand 
import time

# ------------------ Client ------------------
def client_program(orderQueue, messageQueue,nombreCommandesEnAttente, commandesEnAttente, lockSendMessage, lockCompteurCommande,lockArrayCommandeEnAttente):
    commandes_dispo = ['Big Mac', 'Triple Cheese Burger', 'Sundae', 'CBO']
    id = 0
    while True:   
        randomCommandeIndex = rand.randint(0,len(commandes_dispo)-1)
        commande = (id,commandes_dispo[randomCommandeIndex])
        orderQueue.put(commande)
        with lockArrayCommandeEnAttente:
            commandesEnAttente.append(commande)
            with lockCompteurCommande:
                nombreCommandesEnAttente.value +=1
                message = "La commande ({id}, {order}) vient d'être lancée !".format(id=commande[0], order=commande[1]) + '\n'
                message += 'Commandes en liste d\'attente: {listeAttente}'.format(listeAttente=commandesEnAttente) + '\n'
                message += 'Nombre de commandes en liste d\'attente: {nombreListeAttente}'.format(nombreListeAttente=nombreCommandesEnAttente.value)
                messageQueue.put(message)
        lockSendMessage.release()

        #Attente de x secondes avant de lancer une nouvelle commande
        time.sleep(rand.randint(1,3))
        id += 1

    
# ------------------ Major d'Homme ------------------
def majordome_program(messageQueue, nombreCommandesEnAttente, commandesEnAttente,lockCompteurCommande,lockArrayCommandeEnAttente ):
    while True:
        message = messageQueue.get()
        print('------- NEWS -------')
        print(message)
        print('--------------------')







# ------------------ Serveur ------------------
def server_program(i,orderQueue, messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockPickOrderInQueue,lockSendMessage,lockCompteurCommande,lockArrayCommandeEnAttente):
    while True:
        with lockPickOrderInQueue: #un seul serveur prend une commande dans la file à la fois.
            commande = orderQueue.get()
        with lockSendMessage:
            messageQueue.put("Le serveur n°" + str(i) + " s'occupe de la commande: " + "(#" + str(commande[0]) + "," + commande[1] + ")" + " !") 
        time.sleep(rand.randint(1,10))
        with lockSendMessage:
            with lockCompteurCommande:
                nombreCommandesEnAttente.value -= 1
                with lockArrayCommandeEnAttente:
                    commandesEnAttente.remove(commande)
                    message = "La commande ({id}, {order}) a été traitée par le serveur n° {numero} !".format(id=commande[0], order=commande[1], numero=i) + '\n'
                    message += 'Commandes en liste d\'attente: {listeAttente}'.format(listeAttente=commandesEnAttente) + '\n'
                    message += 'Nombre de commandes en liste d\'attente: {nombreListeAttente}'.format(nombreListeAttente=nombreCommandesEnAttente.value)
                    messageQueue.put(message)

            
class ServersManager:
    def __init__(self, nb_servers,programToRun,orderQueue, messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockPickOrderInQueue,lockSendMessage,lockCompteurCommande,lockArrayCommandeEnAttente):

        self.nb_servers = nb_servers
        self.servers = self.createNServer(programToRun,orderQueue, messageQueue,nombreCommandesEnAttente, commandesEnAttente, lockPickOrderInQueue,lockSendMessage,lockCompteurCommande,lockArrayCommandeEnAttente)
        

    
    def createNServer(self,programToRun,orderQueue, messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockPickOrderInQueue,lockSendMessage,lockCompteurCommande, lockArrayCommandeEnAttente):
        servers = []
        if self.nb_servers > 0:
            for i in range(self.nb_servers):
                servers.append(mp.Process(target=programToRun, args=(i,orderQueue,messageQueue,nombreCommandesEnAttente,commandesEnAttente,lockPickOrderInQueue,lockSendMessage,lockCompteurCommande,lockArrayCommandeEnAttente))) 
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

    #Création du compteur du nombre de commandes en attente
    nombreCommandesEnAttente= mp.Value('i', 0)

    #Création de la liste de commande en attente
    commandesEnAttente= mp.Manager().list()

    #Création des verrous de modification de la file d'attente de commande, 
    # d'envoi es messages des serveurs au major d'homme, du compteur de commande et de la liste des commandes en attente
    lockPickOrderInQueue = mp.Lock()
    lockSendMessage = mp.Semaphore(0)
    lockCompteurCommande = mp.Lock()
    lockArrayCommandeEnAttente = mp.Lock()


    #Création du client
    client = mp.Process(target=client_program, args=(orderQueue,messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockSendMessage, lockCompteurCommande, lockArrayCommandeEnAttente))

    #Création des serveurs
    n = 5 #nombre de serveurs
    gestionnaireDesServeurs = ServersManager(n,server_program,orderQueue, messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockPickOrderInQueue,lockSendMessage,lockCompteurCommande, lockArrayCommandeEnAttente)

    #Création du major d'homme
    majordome = mp.Process(target=majordome_program , args=(messageQueue,nombreCommandesEnAttente,commandesEnAttente, lockCompteurCommande, lockArrayCommandeEnAttente))


    #On demarre tous les processus !
    client.start()
    gestionnaireDesServeurs.start()
    majordome.start()
    

    client.join()
    gestionnaireDesServeurs.join()
    majordome.join()
    




 
    




