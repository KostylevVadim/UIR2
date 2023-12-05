import zipfile
import os
from content.read_the_file import Read_the_file
def file_opener():
    # results = [each for each in os.listdir('./in_directory') if '.xml' in each]
    # print('Файлы для анализа')
    # print(*results)
    # x = input('Введите название файла, которых хотите анализировать: ')
    # while x not in results:
    #     print('Файла нет в директории in_directory. Занесите его туда')
    #     x = input('Введите название файла, которых хотите анализировать: ')
    with open('in_directory/file.xml', 'rb') as file:
        
        get_data = Read_the_file(file)
        # get_data.get_format()
        get_data.get_parts_of_article()
        # get_data.get_style()
        # get_data.get_values()
        # get_data.get_literature()
        # get_data.get_additional()
        # get_data.get_structure()
        # get_data.write_file()
        