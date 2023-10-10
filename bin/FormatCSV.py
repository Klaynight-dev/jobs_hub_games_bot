import csv

#
# Vous devrez d'abord
# Supprimer les lignes 1,2,3 et 5
# Du fichier mes-puissances-atteintes-30min-14515774209818-22590.csv
#


# Lire le fichier CSV initial
with open('mes-puissances-atteintes-30min-14515774209818-22590.csv', 'r') as file:
    lines = file.readlines()

# Créer une variable pour stocker la date en cours
current_date = None

# Écrire le nouveau format dans un nouveau fichier CSV
with open('nouveau_fichier.csv', 'w') as file:
    for line in lines:
        # Supprimer les espaces et les sauts de ligne inutiles
        line = line.strip()

        # Vérifier si la ligne est vide
        if not line:
            continue

        # Vérifier si la ligne commence par une date
        if '/' in line:
            # Si la ligne commence par ";;", supprimer ces deux caractères
            if line.endswith(';;'):
                line = line.replace(';;', '', 1)
            
            # Mettre à jour la date en cours
            current_date = line
            continue

        # Séparer la ligne en parties
        parts = line.split(';')

        # Assurez-vous qu'il y ait trois parties (heure, valeur, type) avant de l'écrire
        if len(parts) == 3:
            # Écrire le nouveau format avec la date en cours
            file.write(f'{current_date};{parts[0]};{parts[1]};{parts[2]}\n')

# Fonction pour remplacer les "/" par des "-"
def remplacer_slash_par_tiret(chaine):
    return chaine.replace('/', '-')

# Nom du fichier d'entrée et de sortie
fichier_entree = 'nouveau_fichier.csv'
fichier_sortie = 'mes-puissances-atteintes-30min.csv'

# Ouvrir le fichier CSV initial et le fichier de sortie
with open(fichier_entree, 'r', newline='') as file_in, open(fichier_sortie, 'w', newline='') as file_out:
    reader = csv.reader(file_in, delimiter=';')
    writer = csv.writer(file_out, delimiter=';')
    
    for row in reader:
        nouvelle_ligne = [remplacer_slash_par_tiret(cellule) for cellule in row]
        writer.writerow(nouvelle_ligne)

print("Opération terminée. Le fichier", fichier_sortie, "a été créé avec les '/' remplacés par des '-'.")