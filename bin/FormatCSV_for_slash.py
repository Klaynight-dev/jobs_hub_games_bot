import csv

# Fonction pour remplacer les "/" par des "-"
def remplacer_slash_par_tiret(chaine):
    return chaine.replace('/', '-')

# Nom du fichier d'entrée et de sortie
fichier_entree = 'mes-puissances-atteintes-30min-14515774209818-22590.csv'
fichier_sortie = 'mes-puissances-atteintes-30min.csv'
# Ouvrir le fichier CSV initial et le fichier de sortie
with open(fichier_entree, 'r', newline='') as file_in, open(fichier_sortie, 'w', newline='') as file_out:
    reader = csv.reader(file_in, delimiter=';')
    writer = csv.writer(file_out, delimiter=';')
    
    for row in reader:
        nouvelle_ligne = [remplacer_slash_par_tiret(cellule) for cellule in row]
        writer.writerow(nouvelle_ligne)

print("Opération terminée. Le fichier", fichier_sortie, "a été créé avec les '/' remplacés par des '-'.")