from aifc import Error
import random, time, os, multiprocessing as mp, sys
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x *x + y *y <= 1: count += 1
    return count

if __name__ == '__main__':
    compteur = mp.Value('i',0)
    # Nombre d’essai pour l’estimation
    nb_total_iteration = 10000000
    #Nombre de processus
    N = 3

    for i in range(N):
        if os.fork() == 0:
            nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration // N)
            print(nb_hits)
            with compteur.get_lock():
                compteur.value += nb_hits
            sys.exit(0)

    total_hits = compteur.value   
    print("Valeur estimée Pi par la méthode " + str(N) + "−Processus : ", 4 *total_hits / nb_total_iteration)
    #TRACE :
    # Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604
