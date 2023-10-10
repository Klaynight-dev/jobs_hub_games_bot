import mysql.connector
import matplotlib.pyplot as plt

# Paramètres de connexion à la base de données MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "dm_elouan"
}

# Fonction pour récupérer la consommation totale par mois (heures pleines et heures creuses)
def consommation_par_mois(annee):
    # Établir une connexion à la base de données
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Créer une requête SQL pour obtenir la consommation totale par mois, y compris les heures pleines et les heures creuses
    query = f"""
        SELECT MONTH(`Date de releve de l'index`) AS mois,
               SUM(`Index Heures pleines (kWh)`) AS consommation_hp,
               SUM(`Index Heures creuses (kWh)`) AS consommation_hc
        FROM `mes_index_elec`
        WHERE YEAR(`Date de releve de l'index`) = {annee}
        GROUP BY mois
        ORDER BY mois
    """
    
    
    cursor.execute(query)
    
    # Récupérer les résultats
    results = cursor.fetchall()
    
    # Fermer la connexion à la base de données
    cursor.close()
    connection.close()

    return results

# Fonction pour créer et afficher le graphique
def afficher_graphique(data, annee):
    mois = [row[0] for row in data]
    consommation_hp = [row[1] for row in data]
    consommation_hc = [row[2] for row in data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(mois, consommation_hp, label='Heures Pleines')
    plt.bar(mois, consommation_hc, bottom=consommation_hp, label='Heures Creuses')
    plt.xlabel("Mois")
    plt.ylabel("Consommation totale (kWh)")
    plt.title(f"Consommation totale par mois en {annee}")
    plt.xticks(mois)
    plt.legend()
    plt.show()

# Entrée de l'utilisateur pour l'année
annee = input("Veuillez entrer l'année (par exemple, 2023) : ")

# Appel de la fonction pour récupérer les données
data = consommation_par_mois(annee)

# Affichage du graphique
afficher_graphique(data, annee)
