# Homework_2_Config

Вариант №26

Задание №2

Разработать инструмент командной строки для визуализации графа

зависимостей, включая транзитивные зависимости. Сторонние средства для

получения зависимостей использовать нельзя.

Зависимости определяются по имени пакета платформы .NET (nupkg). Для

описания графа зависимостей используется представление Mermaid.

Визуализатор должен выводить результат на экран в виде графического

изображения графа.

Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Имя анализируемого пакета.

• URL-адрес репозитория.

Все функции визуализатора зависимостей должны быть покрыты тестами.

Описание функций:

def download_file(url, save_path) - функция для скачивания пакетов
    

def get_dependencies(package_name, package_version, depth=0, max_depth=1, all_dependencies=None) - функция для парсирования пакетов
  

def build_mermaid_graph(dependencies) - функция для создания файла графа 
   

def show_png_Graph(mermaid_graph) - функция для создания png графа
   

def cleanup_downloaded_packages(save_directory) - функция очисти пакетов

Тестирование

ТЕСТ 1 

mermaid_cli_path = "C:\Users\Acer\AppData\Roaming\npm\mmdc.cmd"

package_name = "Newtonsoft.Json.Bson"

package_id = "1.0.3"

url = "https://www.nuget.org/api/v2/package/Newtonsoft.Json.Bson/1.0.3"

Скриншот командной строки:

![image](https://github.com/user-attachments/assets/1f046d6a-ea9a-47fe-a3fa-58e9bbce602c)


Скриншот самого графа:

![image](https://github.com/user-attachments/assets/5f93b5af-ff51-44eb-ad6b-0ec030d0f027)

ТЕСТ 2

mermaid_cli_path = r"C:\Users\Acer\AppData\Roaming\npm\mmdc.cmd"

package_name = System.Runtime.Serialization.Json

package_id = 4.3.0

url = https://www.nuget.org/api/v2/package/System.Runtime.Serialization.Json/4.3.0

Скриншот командной строки:

![image](https://github.com/user-attachments/assets/7ab7546d-46b0-4f72-b602-1e55a48d27ba)

Скриншот самого графа:

![image](https://github.com/user-attachments/assets/c4312cce-0544-481b-ada1-7639933cdbc5)

Также вся система протестирована в отдельном файле: https://github.com/Vector-363/Homework_2_Config/blob/Visualizer/TestSystem.py
