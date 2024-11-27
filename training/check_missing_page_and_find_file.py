import os

def check_missing_files(parent_dir):
    for root, dirs, files in os.walk(parent_dir):
        number_files = []
        for file in files:
            try:
                number_files.append(int(file.split('.')[0]))
            except ValueError:
                continue
        
        if number_files:
            number_files.sort()
            missing_numbers = [
                num for num in range(number_files[0], number_files[-1] + 1)
                if num not in number_files
            ]
            if missing_numbers:
                print(f"Missing numbers in {root}: {missing_numbers}")
            else:
                print(f"All numbers are sequential in {root}")

def find_folders_with_file(parent_dir, target_file_name):
    for root, dirs, files in os.walk(parent_dir):
        number_files = []
        for file in files:
            if target_file_name in file: 
                print(f"Folder: '{target_file_name}' : {root}")


parent_directory = r"D:\\"
target_file_name = "999"


# check_missing_files(parent_directory)
find_folders_with_file(parent_directory, target_file_name)