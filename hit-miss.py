import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        # si le point est dans l’unit circle
        if x *x + y *y <= 1: count += 1
    return count
# Nombre d’essai pour l’estimation
nb_total_iteration = 10000000
nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
print("Valeur estimée Pi par la méthode Mono−Processus : ", 4 *nb_hits / nb_total_iteration)
#TRACE :
# Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604
