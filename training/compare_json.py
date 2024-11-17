import json

def compare_json(file1_path, file2_path, output_path):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1:
            data1 = json.load(file1)

        with open(file2_path, 'r', encoding='utf-8') as file2:
            data2 = json.load(file2)

        data2_links = {entry['link'] for entry in data2}

        filtered_data = [
            entry for entry in data1
            if entry['link'] not in data2_links and "r18" not in entry['link']
        ]

        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

        print(f"Fichier comparé avec succès ! Les différences sont écrites dans {output_path}")

    except FileNotFoundError as e:
        print(f"Erreur : Fichier introuvable - {e}")
    except json.JSONDecodeError as e:
        print(f"Erreur : Le fichier n'est pas au format JSON valide - {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

# Chemins des fichiers
file1 = "allseriesv3.json"
file2 = "all_data\\allseriesv2.json"
output = "missed_titles.json"

# Appeler la fonction
compare_json(file1, file2, output)