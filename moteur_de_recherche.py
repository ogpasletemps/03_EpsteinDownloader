from fonctions import download_data, horloge, global_bdd_append

class colors:
    END = "\033[0m"

recherche = input(f"{colors.END}~ Moteur de recherche (saisir une entrée) ->")
occurences = download_data(recherche=recherche)
timestamp = horloge()
global_bdd_append(timestamp, recherche, occurences)