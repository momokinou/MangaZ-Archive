import json


def read_json_file(input_file):
    # Ouverture et lecture du fichier JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        # Charger le contenu du fichier JSON dans un objet Python (list/dictionary)
        data = json.load(file)
    
    # Affichage du contenu du fichier JSON
    return data

# Exemple d'utilisation du script
input_file = 'authors_data.json'  # Chemin vers votre fichier JSON

# Lire le fichier JSON
authors_data = read_json_file(input_file)

# Afficher les données lues
for author in authors_data:
    print(f"Name: {author['author']['name']}, Link: {author['author']['link']}")