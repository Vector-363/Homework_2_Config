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
    if all_dependencies is None:
        all_dependencies = {}
    if depth > max_depth:
        return all_dependencies

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

def cleanup_downloaded_packages(save_directory):
    for filename in os.listdir(save_directory):
        if filename.endswith(".nupkg"):
            filepath = os.path.join(save_directory, filename)
            try:
                os.remove(filepath)  # Or shutil.rmtree(filepath) if it's a directory
                print(f"Удален файл: {filepath}")
            except OSError as e:
                print(f"Ошибка при удалении файла {filepath}: {e}")

def Test_1():
    package_name = "System.Runtime.Serialization.Json"
    package_id = "4.3.0"
    result = get_dependencies(package_name, package_id)
    assert result == {
        'System.IO.4.3.0': {'System.Threading.Tasks.4.3.0', 'System.Text.Encoding.4.3.0',
                            'Microsoft.NETCore.Targets.1.1.0', 'Microsoft.NETCore.Platforms.1.1.0',
                            'System.Runtime.4.3.0'},
        'Microsoft.NETCore.Platforms.1.1.0': set(),
        'Microsoft.NETCore.Targets.1.1.0': set(),
        'System.Runtime.4.3.0': set(),
        'System.Text.Encoding.4.3.0': set(),
        'System.Threading.Tasks.4.3.0': set(),
        'System.Private.DataContractSerialization.4.3.0': {'System.Threading.4.3.0', 'System.Diagnostics.Debug.4.3.0',
                                                           'System.Reflection.TypeExtensions.4.3.0',
                                                           'System.Xml.XDocument.4.3.0',
                                                           'System.Reflection.Emit.Lightweight.4.3.0',
                                                           'System.Text.Encoding.Extensions.4.3.0',
                                                           'System.Reflection.Emit.ILGeneration.4.3.0',
                                                           'System.Reflection.Primitives.4.3.0',
                                                           'System.Reflection.4.3.0', 'System.Text.Encoding.4.3.0',
                                                           'System.IO.4.3.0', 'System.Collections.4.3.0',
                                                           'System.Runtime.4.3.0', 'System.Xml.XmlSerializer.4.3.0',
                                                           'System.Text.RegularExpressions.4.3.0',
                                                           'System.Runtime.Serialization.Primitives.4.3.0',
                                                           'System.Threading.Tasks.4.3.0',
                                                           'System.Xml.ReaderWriter.4.3.0',
                                                           'System.Reflection.Extensions.4.3.0', 'System.Linq.4.3.0',
                                                           'System.Xml.XmlDocument.4.3.0',
                                                           'System.Collections.Concurrent.4.3.0',
                                                           'System.Runtime.Extensions.4.3.0',
                                                           'Microsoft.NETCore.Platforms.1.1.0',
                                                           'System.Resources.ResourceManager.4.3.0',
                                                           'System.Globalization.4.3.0'},
        'System.Reflection.TypeExtensions.4.3.0': set(),
        'System.Runtime.Serialization.Primitives.4.3.0': set(),
        'System.Xml.XmlDocument.4.3.0': set(),
        'System.Collections.4.3.0': set(),
        'System.Collections.Concurrent.4.3.0': set(),
        'System.Diagnostics.Debug.4.3.0': set(),
        'System.Globalization.4.3.0': set(),
        'System.Linq.4.3.0': set(),
        'System.Reflection.4.3.0': set(),
        'System.Reflection.Extensions.4.3.0': set(),
        'System.Reflection.Primitives.4.3.0': set(),
        'System.Resources.ResourceManager.4.3.0': set(),
        'System.Runtime.Extensions.4.3.0': set(),
        'System.Text.Encoding.Extensions.4.3.0': set(),
        'System.Text.RegularExpressions.4.3.0': set(),
        'System.Threading.4.3.0': set(),
        'System.Xml.ReaderWriter.4.3.0': set(),
        'System.Xml.XDocument.4.3.0': set(),
        'System.Xml.XmlSerializer.4.3.0': set(),
        'System.Reflection.Emit.ILGeneration.4.3.0': set(),
        'System.Reflection.Emit.Lightweight.4.3.0': set(),
        'System.Runtime.Serialization.Json.4.3.0': {'System.Private.DataContractSerialization.4.3.0', 'System.IO.4.3.0',
                                                    'System.Runtime.4.3.0'}
    }
    cleanup_downloaded_packages(r"C:\Users\Acer\PycharmProjects\Homework_2_Config")

def Test_2():
    package_name = "Newtonsoft.Json.Bson"
    package_id = "1.0.3"
    result = get_dependencies(package_name, package_id)
    assert result  == {
        'Newtonsoft.Json.13.0.1': {'System.Runtime.Serialization.Formatters.4.3.0', 'System.Xml.XmlDocument.4.3.0',
                                   'System.ComponentModel.TypeConverter.4.3.0',
                                   'System.Runtime.Serialization.Primitives.4.3.0', 'Microsoft.CSharp.4.3.0',
                                   'NETStandard.Library.1.6.1'},
        'Microsoft.CSharp.4.3.0': set(),
        'NETStandard.Library.1.6.1': set(),
        'System.ComponentModel.TypeConverter.4.3.0': set(),
        'System.Runtime.Serialization.Primitives.4.3.0': set(),
        'System.Runtime.Serialization.Formatters.4.3.0': set(),
        'System.Xml.XmlDocument.4.3.0': set(),
        'Newtonsoft.Json.Bson.1.0.3': {'Newtonsoft.Json.13.0.1', 'NETStandard.Library.1.6.1'}
    }
    cleanup_downloaded_packages(r"C:\Users\Acer\PycharmProjects\Homework_2_Config")


Test_1()
Test_2()


print("Все тесты пройдены!")

