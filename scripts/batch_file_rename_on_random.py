import os
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def rename_files_with_random_numbers(folder_path):
    file_list = os.listdir(folder_path)
    
    for old_name in file_list:
        if os.path.isfile(os.path.join(folder_path, old_name)):
            file_extension = os.path.splitext(old_name)[1]
            new_name = generate_random_string(8) + file_extension
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {old_name} to {new_name}")

def main():
    folder_path = r"C:\xxx"  # Path to the folder containing files
    
    rename_files_with_random_numbers(folder_path)

if __name__ == "__main__":
    main()
