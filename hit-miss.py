import random, time, os, multiprocessing as mp, sys, math
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
    nb_total_iteration = 50000000
    #Nombre de processus
    N = 10
    time1 = time.time()
    for i in range(N):
        if os.fork() == 0:
            nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration // N)
            with compteur.get_lock():
                compteur.value += nb_hits
            sys.exit(0)

    for i in range(N):
        os.wait()
        
    total_hits = compteur.value   
    time2 = time.time()
    erreur = 1/math.sqrt(nb_total_iteration)
    print('Nombre de fléchettes lancées: ', nb_total_iteration)
    print("Valeur estimée Pi par la méthode " + str(N) + "−Processus : ", 4 *total_hits / nb_total_iteration)
    print('Erreur de calcul: ', erreur)
    print("Temps de calcul:", round(time2-time1,3), "secondes")
