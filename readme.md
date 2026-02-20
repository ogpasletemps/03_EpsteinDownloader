# EpsteinDowloader

Ce logiciel à pour but d'aider au téléchargement des données présentes dans les **"Epstein files"** publiés par le departement de la justice du gouvernement américain.

Le logiciel utilise le même fonctionnement que le site web de référence, il suffit de taper **un mot, une combinaison de mots ou un nom propre** pour effectuer une recherche.

Si le champ recherché est présent dans la base de données du département de la justice, tout les fichiers liés seront téléchargés et placés dans le dossier du même nom.

Deux modes de téléchargement sont proposés : 
- Une recherche unique, avec le moteur de recherche.
- Une recherche multiple, avec le téléchargement en batch.

La base de données **base_de_donnees_globale.xlsx** recense toutes les recherches effectués via le logiciel.

# Installation

L'installation du logiciel est détaillé ci-dessous.  

```
Etape 1 - Telechargement de python version 3.12.10
Veillez à cocher l'ajout de .path lors de l'installation de python.
Url ci-dessous.
```
Lien pour le téléchargement de [Python 3.12.10](https://www.python.org/downloads/release/python-31210/)
```
Etape 2 - Téléchargement de la dernière release disponible sur github en zip.
```
```
Etape 3 - Execution du fichier init.bat
```
Une fois les étapes réalisés le logiciel est prêt à être utilisé.

# Utilisation
  
## Recherche unique.

Pour utiliser le moteur de recherche veuillez suivre la marche suivante.

```
Etape 1 - Execution de run.bat
```
```
Etape 2 - Saisie de 0 pour aller au mode de recherche unique.
```
```
Etape 3 - Saisie du champ de recherche souhaité.
```
Les données seront ensuite téléchargées.

## Recherche multiple.

Pour utiliser la recherche en batch veuillez suivre la marche suivante.

```
Etape 1 - Remplir les champs de recherche souhaités dans le fichier batch.xlsx
```
```
Etape 2 - Execution de run.bat
```
```
Etape 3 - Saisie de 1 pour aller au mode de recherche multiple.
```
Les données seront ensuite téléchargées.

# FAQ

Pour tout questions concernant le dépannage ou l'utilisation veuillez me contacter sur mon twitter **@ogpasletemps**.