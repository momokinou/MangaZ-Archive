import json

# Fonction pour inverser le contenu du JSON
def reverse_json_content(input_file, output_file):
    # Lire le fichier JSON d'entrée
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Inverser l'ordre si data est une liste ou un dictionnaire
    if isinstance(data, list):
        data_reversed = data[::-1]  # Liste inversée
    elif isinstance(data, dict):
        data_reversed = {k: data[k] for k in reversed(data)}  # Dictionnaire inversé
    else:
        print("Le format JSON n'est ni une liste ni un dictionnaire.")
        return

    # Sauvegarder le contenu inversé dans le nouveau fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data_reversed, f, ensure_ascii=False, indent=4)

    print(f"Contenu inversé enregistré dans {output_file}.")

# Exemples d'utilisation
input_file = 'allseriesv2.json'      # Remplacer par le nom de votre fichier JSON d'entrée
output_file = 'allseriesreversed.json'    # Nom du fichier de sortie

reverse_json_content(input_file, output_file)