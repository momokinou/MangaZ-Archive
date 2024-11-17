import json
import os

def split_json(input_file, output_prefix, lines_per_file=300):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        total_lines = len(data)
        
        for i in range(0, total_lines, lines_per_file):
            part_number = i // lines_per_file + 1
            chunk = data[i:i + lines_per_file]
            
            output_file = f"{output_prefix}_part{part_number+20}.json"
            
            with open(output_file, 'w', encoding='utf-8') as output:
                json.dump(chunk, output, ensure_ascii=False, indent=4)
            
            print(f"Created: {output_file}")

    except FileNotFoundError as e:
        print(f"Can't find file - {e}")
    except json.JSONDecodeError as e:
        print(f"JSON Invalid- {e}")
    except Exception as e:
        print(f"Error:{e}")

input_file = "missed_titles.json"

output_prefix = "allseries"

split_json(input_file, output_prefix)