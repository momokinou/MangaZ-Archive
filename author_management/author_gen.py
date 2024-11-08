import json

def generate_json_from_file(input_file, output_file):
    # Création d'une liste pour stocker les données sous forme de dictionnaires
    authors_data = []
    
    # Ouverture du fichier texte en mode lecture
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Supprimer les espaces et retours à la ligne inutiles
            line = line.strip()
            if '>' in line:
                # Séparer la ligne au niveau du ">"
                link, name = line.split('>', 1)
                
                # Créer un dictionnaire pour chaque auteur avec les informations de "name" et "link"
                author_data = {
                    "author": {
                        "name": name,
                        "link": 'https://www.mangaz.com' + link
                    }
                }
                authors_data.append(author_data)
    
    # Enregistrer le résultat dans un fichier JSON
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(authors_data, json_file, ensure_ascii=False, indent=4)

# Exemple d'utilisation du script
input_file = 'tmp.txt'  # Chemin vers votre fichier texte
output_file = './authors_data.json'  # Chemin vers le fichier de sortie JSON

generate_json_from_file(input_file, output_file)