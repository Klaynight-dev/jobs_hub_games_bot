import requests
import webbrowser
import folium
import csv
import numpy as np

# Fonction pour importer des données depuis une URL au format JSON
def import_data(url):
    response = requests.get(url)
    assert response.status_code == 200, f"La requête a échoué avec le code d'état : {response.status_code}"
    if response.status_code == 200:
        return response.json()  # Renvoie les données JSON si la requête réussit
    else:
        print("La requête a échoué avec le code d'état:", response.status_code)
        return None

# Fonction pour charger les données depuis un fichier CSV
def load_data_from_csv(file_path):
    with open(file_path, 'r') as f:
        return np.array(list(csv.reader(f, delimiter=";")))

# Fonction pour créer une carte Folium
def create_map():
    return folium.Map(location=[46.227638, 2.213749], zoom_start=6)

# Fonction principale
def main():
    # Charger les données de préfectures depuis un fichier CSV
    donnees = load_data_from_csv('prefectures.csv')
    
    # Demander à l'utilisateur de saisir le code département recherché
    code_departement = input("Entrer le code du département recherché : ")

    # Obtenir les données du département spécifié depuis une API gouvernementale
    url_Dep = f"https://geo.api.gouv.fr/departements/{code_departement}?fields=codeRegion"
    data = import_data(url_Dep)

    if data is None:
        print("Échec de la récupération des données du département.")
        return  # Arrêtez le programme si la requête a échoué

    # Extraire le code de la région associée au département
    codeR = data['codeRegion']
    print("Données du département sélectionné :")
    print(data)
    nom_dep_prime = data['nom']

    # Obtenir les données des départements de la région associée
    url_Reg = f"https://geo.api.gouv.fr/regions/{codeR}/departements?fields=nom"
    data = import_data(url_Reg)
    print("\nDonnées des départements de la région associée :")
    print(data)

    # Créer une carte Folium
    m = create_map()

    # Parcourir les données des départements de la région et afficher des marqueurs sur la carte
    for trouver in data:
        num_dep = trouver['code']
        nom_dep = trouver['nom']

        # Rechercher les données de préfecture correspondantes dans le fichier CSV
        for i in range(len(donnees)):
            if num_dep == donnees[i][0]:
                print("\nDonnées de la préfecture du département :")
                print("Nom de départment :", donnees[i][3])
                print("Nom de la préfecture :", donnees[i][2])
                print("Numéro de département :", donnees[i][0])
                print("Latitude :", donnees[i][4])
                print("Longitude :", donnees[i][5])
                nom_pref = donnees[i][2]
                latitude = donnees[i][4]
                longitude = donnees[i][5]

        a = f"{nom_pref} {nom_dep} ({num_dep})"

        # Définir la couleur du marqueur en fonction du département recherché
        couleur = 'black' if code_departement == num_dep else 'blue'

        # Ajouter un marqueur à la carte
        folium.Marker([latitude, longitude], tooltip=nom_pref, icon=folium.Icon(color=couleur), popup=a, tiles="Stamen Terrain",).add_to(m)

    # Enregistrer la carte au format HTML
    m.save('carte.html')

    # Ouvrir la carte dans le navigateur par défaut
    webbrowser.open('carte.html')

# Exécutez la fonction principale si le fichier est exécuté en tant que script
if __name__ == "__main__":
    main()