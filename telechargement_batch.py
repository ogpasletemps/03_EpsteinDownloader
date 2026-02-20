import os
import pandas as pd
from pathlib import Path
from fonctions import download_data, horloge, global_bdd_append

class colors:
    END = "\033[0m"

base = os.getcwd()
path = Path(base + r"/batch/batch.xlsx")
df = pd.read_excel(path)
liste_mot = list(df["mot"])
iterations = len(liste_mot)

for i in range(iterations):
    recherche = liste_mot[i]
    occurences = download_data(recherche=recherche)
    timestamp = horloge()
    global_bdd_append(timestamp, recherche, occurences)



