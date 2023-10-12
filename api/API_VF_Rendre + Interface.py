import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
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
def generate_map():
    code_departement = code_departement_entry.get()
    
    # Charger les données de préfectures depuis un fichier CSV
    donnees = load_data_from_csv('prefectures.csv')
    
    # Obtenir les données du département spécifié depuis une API gouvernementale
    url_Dep = f"https://geo.api.gouv.fr/departements/{code_departement}?fields=codeRegion"
    data = import_data(url_Dep)

    if data is None:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Échec de la récupération des données du département.")
        return  # Arrêtez le programme si la requête a échoué

    # Extraire le code de la région associée au département
    codeR = data['codeRegion']
    result_text.delete(1.0, tk.END)
    print(f"Données du département sélectionné:\n{data}")
    nom_dep_prime = data['nom']

    # Obtenir les données des départements de la région associée
    url_Reg = f"https://geo.api.gouv.fr/regions/{codeR}/departements?fields=nom"
    data = import_data(url_Reg)
    print(f"\nDonnées des départements de la région associée:\n{data}")

    # Créer une carte Folium
    m = create_map()

    # Parcourir les données des départements de la région et afficher des marqueurs sur la carte
    for trouver in data:
        num_dep = trouver['code']
        nom_dep = trouver['nom']

        # Rechercher les données de préfecture correspondantes dans le fichier CSV
        for i in range(len(donnees)):
            if num_dep == donnees[i][0]:
                result_text.insert(tk.END, "\n\nDonnées de la préfecture du département:")
                result_text.insert(tk.END, f"\nNom de départment : {donnees[i][3]}")
                result_text.insert(tk.END, f"\nNom de la préfecture : {donnees[i][2]}")
                result_text.insert(tk.END, f"\nNuméro de département : {donnees[i][0]}")
                result_text.insert(tk.END, f"\nLatitude : {donnees[i][4]}")
                result_text.insert(tk.END, f"\nLongitude : {donnees[i][5]}")
                nom_pref = donnees[i][2]
                latitude = donnees[i][4]
                longitude = donnees[i][5]

        a = f"{nom_pref} {nom_dep} ({num_dep})"

        # Définir la couleur du marqueur en fonction du département recherché
        couleur = 'black' if code_departement == num_dep else 'blue'

        # Ajouter un marqueur à la carte
        folium.Marker([latitude, longitude], tooltip=nom_pref, icon=folium.Icon(color=couleur), popup=a, tiles="Stamen Terrain").add_to(m)

    # Enregistrer la carte au format HTML
    m.save('carte.html')
    result_text.insert(tk.END, "\n\nLa carte a été générée et enregistrée sous 'carte.html'.")
    webbrowser.open('carte.html')

# Création de la fenêtre principale
window = tk.Tk()
window.title("Générateur de Carte")

# Configurez la police pour toute l'interface
font_style = ("Liberation Serif", 12)

# Création d'un style personnalisé pour les boutons
button_style = ttk.Style()
button_style.configure("Custom.TButton", font=font_style)

# Création de l'interface utilisateur
code_departement_label = ttk.Label(window, text="Code du département", font=font_style)
code_departement_entry = ttk.Entry(window, font=font_style)
generate_button = ttk.Button(window, text="Générer la carte", command=generate_map, style="Custom.TButton")

# Créez un widget de texte défilant pour afficher les résultats
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=15, font=font_style)

# Placement des composants d'interface utilisateur
code_departement_label.grid(row=0, column=0, padx=10, pady=10)
code_departement_entry.grid(row=0, column=1, padx=10, pady=10)
generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Démarrage de la boucle principale de l'interface
window.mainloop()