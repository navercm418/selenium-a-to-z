import os

def delete_files_except(directory, exceptions):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename not in exceptions:
            os.remove(file_path)
            print(f"Deleted file: {filename}")

if __name__ == "__main__":
    directory_path = "."  # Replace with the actual directory path
    excluded_files = ["AtoZ.py", "googlemaps.py", "main.py", "myutils.py", "README.md", "zzCleanup.py"]  # Replace with your list of exceptions
    delete_files_except(directory_path, excluded_files)
