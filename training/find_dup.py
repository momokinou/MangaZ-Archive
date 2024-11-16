import json
from collections import defaultdict

def find_duplicates(json_file):
    # Charger les données du fichier JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Utiliser un dictionnaire pour compter les occurrences de chaque titre
    title_count = defaultdict(list)

    # Parcourir chaque entrée et ajouter les liens associés à chaque titre
    for entry in data:
        title = entry['title']
        link = entry['link']
        title_count[title].append(link)

    # Extraire et afficher les titres avec des doublons
    duplicates = {title: links for title, links in title_count.items() if len(links) > 1}

    if duplicates:
        print("Doublons trouvés:")
        for title, links in duplicates.items():
            print(f"\nTitre : {title}")
            for link in links:
                print(f" - Lien : {link}")
    else:
        print("Aucun doublon trouvé.")

# Utilisation
find_duplicates('allseriesv2.json')