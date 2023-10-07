from work_on_file import Work_on_file
def file_opener():
    with open('file.xml', 'r+',encoding='utf-8') as file:
        # Разбираем XML
        in_body = 0
        result = open('result.xml', 'w+',encoding='utf-8')
        result = Work_on_file.set_Times_new_roman_everywhere(file, result)
        result.close()