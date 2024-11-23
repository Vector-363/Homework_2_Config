import requests
import argparse
import subprocess
#Тест 1
# mermaid_cli_path = r"C:\Users\Acer\AppData\Roaming\npm\mmdc.cmd"
# package_name = "Newtonsoft.Json.Bson"
# package_id = "1.0.3"
# url = "https://www.nuget.org/api/v2/package/Newtonsoft.Json.Bson/1.0.3"

import requests
import os
import argparse

def download_file(url, save_path):
    if os.path.exists(save_path):
        print(f"Файл {save_path} уже существует. Пропуск скачивания.")
        return  # Exit if the file already exists

    try:
        response = requests.get(url, stream=True)  # Stream for large files
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192): #Chunking for efficient download
                file.write(chunk)
        print(f"Файл успешно скачан и сохранен в: {save_path}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка при запросе: {err}") #More specific exception handling
    except Exception as err:
        print(f"Произошла ошибка: {err}")

def get_dependencies(package_name, package_version, depth=0, max_depth=1, all_dependencies=None):
    url = f"https://www.nuget.org/api/v2/package/{package_name}/{package_version}"  # Corrected URL
    save_directory = r"C:\Users\Acer\PycharmProjects\Homework_2_Config"  # Update to your directory
    save_file_path = os.path.join(save_directory, f"{package_name}.{package_version}.nupkg")
    download_file(url, save_file_path)

    nupkg_path = save_file_path
    if not os.path.exists(nupkg_path):
        print(f"{nupkg_path} не найден.")
        return all_dependencies



def main():
    parser = argparse.ArgumentParser(description="Visualize .NET package dependencies using Mermaid.")
    parser.add_argument("path_to_mermaid", help="Path to the graph visualization tool (e.g., mermaid-cli)")
    parser.add_argument("package_name", help="Name of the .NET package")
    parser.add_argument("package_version", help=".NET package version")
    parser.add_argument("url_repos", help=".NET package url")
    args = parser.parse_args()





if __name__ == "__main__":
    main()

