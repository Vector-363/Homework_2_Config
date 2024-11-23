#Тест 1
# mermaid_cli_path = r"C:\Users\Acer\AppData\Roaming\npm\mmdc.cmd"
# package_name = "Newtonsoft.Json.Bson"
# package_id = "1.0.3"
# url = "https://www.nuget.org/api/v2/package/Newtonsoft.Json.Bson/1.0.3"

#Тест2
# mermaid_cli_path = r"C:\Users\Acer\AppData\Roaming\npm\mmdc.cmd"
# package_name = System.Runtime.Serialization.Json
# package_id = 4.3.0
# url = https://www.nuget.org/api/v2/package/System.Runtime.Serialization.Json/4.3.0


import requests
import os
import argparse
import xml.etree.ElementTree as ET
import zipfile

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

    try:
        with zipfile.ZipFile(nupkg_path, 'r') as zip_ref:
            nuspec_file = [f for f in zip_ref.namelist() if f.endswith('.nuspec')]
            if nuspec_file:
                with zip_ref.open(nuspec_file[0]) as file:
                    tree = ET.parse(file)
                    root = tree.getroot()
                    namespaces = {'ns': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
                    dependencies_set = set()
                    for dependency in root.findall(".//ns:dependency", namespaces):
                        dep_id = dependency.get('id')
                        dep_version = dependency.get('version')
                        if dep_id and dep_version:
                            dep_package = f"{dep_id}.{dep_version}"  # Corrected formatting
                            dependencies_set.add(dep_package)
                            if dep_package not in all_dependencies:
                                all_dependencies[dep_package] = set()
                                get_dependencies(dep_id, dep_version, depth + 1, max_depth, all_dependencies)
                    all_dependencies[f"{package_name}.{package_version}"] = dependencies_set
    except Exception as e:
        print(f"Ошибка при обработке {package_name}.{package_version}: {e}")

    return all_dependencies

def build_mermaid_graph(dependencies):
    if not isinstance(dependencies, dict):
        return "Error: Invalid input. 'dependencies' must be a dictionary."

    for package, deps in dependencies.items():
        if not isinstance(deps, set):
            return "Error: Invalid input. Dependency values must be sets."

    graph = "graph LR;\n"

    # Добавляем узлы (пакеты) с подграфами
    for package_name_version in dependencies:
        package_name, package_version = package_name_version.rsplit(".", 1)  # Разделяем на имя и версию
        graph += f'subgraph "{package_name} ({package_version})"\n'  # Подграф с номером версии
        graph += f"{package_name_version}\n"
        graph += "end\n"

    # Добавляем ребра (зависимости)
    for package_name_version, deps in dependencies.items():
        for dep in deps:
            graph += f"{package_name_version} --> {dep}\n"

    return graph

def show_png_Graph(mermaid_graph):
    with open("graph.mmd", "w") as f:
        f.write(mermaid_graph)
    print("Graph saved to graph.mmd. Generating PNG...")
    os.system(f"mmdc -i graph.mmd -o graph.png")
    print("PNG generated as graph.png. Opening the image...")
    os.system("start graph.png" if os.name == "nt" else "open graph.png")

def cleanup_downloaded_packages(save_directory):
    """Removes all downloaded .nupkg files from the specified directory."""
    for filename in os.listdir(save_directory):
        if filename.endswith(".nupkg"):
            filepath = os.path.join(save_directory, filename)
            try:
                os.remove(filepath)  # Or shutil.rmtree(filepath) if it's a directory
                print(f"Удален файл: {filepath}")
            except OSError as e:
                print(f"Ошибка при удалении файла {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Visualize .NET package dependencies using Mermaid.")
    parser.add_argument("path_to_mermaid", help="Path to the graph visualization tool (e.g., mermaid-cli)")
    parser.add_argument("package_name", help="Name of the .NET package")
    parser.add_argument("package_version", help=".NET package version")
    parser.add_argument("url_repos", help=".NET package url")
    args = parser.parse_args()

    dependencies = get_dependencies(args.package_name, args.package_version)  # поиск зависимостей
    mermaid_graph = build_mermaid_graph(dependencies)  # создание файла для графа
    show_png_Graph(mermaid_graph)  # создание png и открытие его

    cleanup_downloaded_packages(r"C:\Users\Acer\PycharmProjects\Homework_2_Config")  # очистка скачанных пакетов



if __name__ == "__main__":
    main()
