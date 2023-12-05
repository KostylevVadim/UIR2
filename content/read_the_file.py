
import lxml.etree as et
import re


class Read_the_file:
    __recognized_fonts=['Times New Roman',
                     'Calibri', 'Arial']
    __recognized_lit_templates = [
        'ГОСТ Р 7.0.100 -2018',
        'ГОСТ Р 7.0.5 -2008',
        'ГОСТ Р 7.0.5 --2008',
        'Ванкуверский стиль',
        'Vancouver',
        'Harvard',
        'Council of Biology Editors',
        'GSA',
        'MLA',
        'MHRA',
        'Chicago',
        'AMS',
        'ASME',
        'AMA',
        'NLM',
        'APA',
        'APSA',
        'ASABE',
        'ASA',
        'AMA',
        'AIP',
        'IEEE',
        'ALWD'
    ]
    __recognized_formats = 'xf, plt, gif, cgm, cdr, eps, jpg, pcd, pct, drw, pcx, png, tif, tga, dib, bmp, rle, wmf, emf, wpg'.split(', ')
    __recognized_struct_elems = [
        'УДК',
        'Заглавие',
        'Заголовок',
        'Название статьи',
        'Сведения об авторе/авторах',
        'Список организаций',
        'e-mail',
        'Аннотация',
        'Ключевые слова',
        'Основной текст статьи',
        'Список литературы',
        'Автор',
        'Сведения об автор',
        'текст статьи',
        'Графический материал',
        'формул',
        'таблиц',
        'рисун',
        'Формул'
    ]
    
    __namespaces = {'w':"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lang = 'rus'
    __recognized_elems = ['Название статьи', 'Автор', 'Рис','Изобр', 'Аннотация', 'Ключевые слова', 'Список литературы', 'текст']
    def __init__(self, file):
        self.__etree = et.parse(file)
        self.__root =  self.__etree.getroot()
        self.__requirements_of_format ={
            'Format': None,
            #  Язык статьи один, требуется в конце + анатация и все такое, отедельные на английском. Я предлагаю. 
            # У журналов нет классификации. 
            'lang': None,
            'Numeration': None
        }
        # Для удобства пользователя - бред, не было в задании, пользователя убрать, машиннообрабатываемое представление.
        self.__requirements_of_style = {
            'Font': None,
            'kegl': None,
            'indent': None,
            'interval_string': None,
            'interval_par': None,
            'indent_first': None,
            
            'field': None,
            'jc': None

        }
        # Проверить список ВАК, диалог, разное посмотреть. Зонт, корпусная лингвистика. Список журналов. Журналы мифи.
        # Рассмотреть мифи, инженерная физика. КИИ. Нейроинформатика.
        # Перевести в 0 и 1. Таблица в которой структура заполнена на основе разных статей.
        # Нормальные структуры данных.
        self.__requirements_of_structure = {
            'Title': '',
            # Как проработать к статье.
            'Author': '',
            'Annotation': '',
            'Contacts': ''
        }
        self.__requirements_of_literature = {
            'Temlate_name' : '',
            # точная 
            'Uses examples': []
        }
        self.__additional = {
            'tables': '',
            'pic': '',
            'formula':''
        }
        # Представление требований. Решить. Прочистить
        # Таблицы для нормальных журналов. BICA
        self.__requirements_of_value = {
            'Min_number_of_pages': None,
            'Min_lit_number' : None,
            'Pic_number' : None,
            'Tab_number' : None,
            'Key_word_num': None
        }
        
    def __get_all_paragraphs(self):
        elements = self.__root.findall('.//w:p',Read_the_file.__namespaces)
        return elements

    def __get_text_from_element(self,element):
        # print(element)
        text = element.findall('.//w:t',Read_the_file.__namespaces)
        txt = ''
        for part in text:
            txt+=part.text
        return txt     
        
        
    def write_file(self):
        # file = open('result.txt','r+')
        with open('out/result.txt', "w+", encoding="utf-8") as file:
            file.write('Требования формата\n')
            for key, value in self.__requirements_of_format.items():
                file.write(key+' '+str(value)+'\n')
            file.write('Требования стиля\n')
            for key, value in self.__requirements_of_style.items():
                file.write(key+' '+str(value)+'\n')
            file.write('Количественные требования\n')
            for key, value in self.__requirements_of_value.items():
                file.write(key+' '+str(value)+'\n')

            file.write('Требования к литературе')
            for key,value in self.__requirements_of_literature.items():
                file.write(key+' '+str(value)+'\n')
            
            file.write('Требования к структуре')

            for key, value in self.__requirements_of_structure.items():
                file.write(key+' '+str(value)+'\n')


            file.write('Требования оформления элементов статьи\n')

            file.write('table'+' '+str(self.__additional['tables'])+'\n')
            file.write('pic'+' '+str(self.__additional['pic'])+'\n')
            file.write('formula'+' '+str(self.__additional['formula'])+'\n')
            # print(str(self.__additional['tables']))
            return file
    
    def get_format(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            # print(text)
            # pattern = r'a\d\+'
            text_arr = text.split(' ')
            for i, word in enumerate(text_arr):
                # print(word)
                
                if 'А4' in word or 'А3' in word or 'А0' in word or 'А1' in word or 'А2' in word or 'А5' in word or 'А6' in word:
                    self.__requirements_of_format['Format']= word
                
                if 'нумерация' in word.lower() and self.__requirements_of_format['Numeration'] is None:
                    j = i
                    st = ''

                    for x in range(j, len(text_arr)):
                        st += str(text_arr[x])+ ' '
                        if '.' in text_arr[x] or ';' in text_arr[x] or '\n' in text_arr[x]:
                            break
                    
                    self.__requirements_of_format['Numeration']= st
        # print(self.__requirements_of_format)

    # Добавить оформление элементов статей. 
    # Улучшить дополнения по поводу оформления для рисунков, статей, таблиц

    def get_style(self):
        paragraphs = self.__get_all_paragraphs()
        # print(paragraphs)
        inter = 0
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            # print(text)
            
            list_of_sentences = text.split('.')
            for i, sent in enumerate(list_of_sentences):
                
                regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                sent_list = x.split(' ')
                # print('Поля')
                y = 'верхнее' in x.lower() or 'нижнее' in x.lower() or 'правое' in x.lower() or 'левое' in x.lower()
                if 'поля' in x.lower() or 'поле' in x.lower() and y:
                    # print(y)
                    print('Поля')
                    for i, elem in enumerate(sent_list):
                        # print(elem, elem.lower() == 'верхнее', elem.lower() == 'нижнее', elem.lower() == 'правое', elem.lower() == 'левое')
                        if elem.lower() == 'верхнее':
                            print('here')
                            for j in range(i, len(sent_list)):
                                # print(sent_list[j])
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                        elif elem.lower() == 'нижнее':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                        elif elem.lower() == 'правое':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                        elif elem.lower() == 'левое':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                        elif y == False:
                            m =0
                            # print(sent_list)
                            for j, word in enumerate(sent_list):
                                # print('поля' in word.lower(), word)
                                if 'поле' in word.lower() or 'поля' in word.lower():
                                    m = j
                                if j> m and word[0].isdigit() and 'см' in word:
                                    print(word)
                                    break
                if 'отступ' in x.lower() and ('первой' in x.lower() or 'красной' in x.lower()):
                    
                    for i, elem in enumerate(sent_list):
                        if 'отступ' in elem.lower():
                            flag = 0
                            for j in range(i, len(sent_list)):
                                # print(sent_list[j]
                                if 'первой' in sent_list[j] or 'красной' in sent_list[j]:
                                    flag = 1
                                if sent_list[j][0].isdigit() and flag == 1:
                                    print('Отступ красной строки')
                                    print(sent_list[j])
                                    break
                # print('Times New Roman' in x)
                elif 'отступ' in x.lower():
                    print('Отступ')
                    n = 'справа' in x.lower() or 'слева' in x.lower() or 'сверху' in x.lower() or 'снизу' in x.lower()
                    if n:
                        for n, elem in enumerate(sent_list):
                            if 'отступ' in elem.lower():
                                for j in range(n, len(sent_list)):
                                    # print(sent_list[j]
                                    if 'справа' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'слева' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'сверху' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'снизу' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                        

                                    
                    else:
                        for i, elem in enumerate(sent_list):
                            if 'отступ' in elem.lower():
                                for j in range(i, len(sent_list)):
                                    # print(sent_list[j]
                                    if sent_list[j][0].isdigit():
                                        print(sent_list[j])
                                        break
                                            
                for font in self.__recognized_fonts:
                    if font in x:
                        print('Font')
                        print(font)
                if 'шрифт' in x.lower() or 'кегль' in x.lower():
                    
                    for j in range(i, len(sent_list)):
                        if sent_list[j][0].isdigit():
                            print('Кегль')
                            print(sent_list[j])
                            break
                fl = 0
                
                if 'выравнивание' in x.lower() and fl ==0:
                    # print(fl, sent_list, i)
                    print('Выравнивание')
                    for j in range(i, len(sent_list)):
                        if 'ширине' in sent_list[j]:
                            print('ширине')
                        elif 'левому' in sent_list[j]:
                            print('левому краю')
                        elif 'правому' in sent_list[j]:
                            print('правому краю')
                        elif 'центру' in sent_list[j]:
                            print('центру')
                
                if 'интервал' in x.lower() and ('абзац' not in x.lower()) and inter == 0:
                    print('Межстрочный интервал')
                    for j, word in enumerate(sent_list):
                        u = 0
                        if 'интервал' in word.lower():
                            # print(j, word)
                            t = j
                            fl = 0
                            while sent_list[t][-1]!=',':
                                
                                if sent_list[t][0].isdigit():
                                    fl =1
                                    u = 1
                                    print(sent_list[t])
                                    inter = 1
                                    break
                                t+=1
                                if t>=len(sent_list):
                                    break
                            if fl == 0:
                                # print('here', 'одинарн' in x, x)
                                if 'полуторны' in x or 'полтора' in x:
                                    print('1,5')
                                    u = 1
                                    inter = 1
                                if 'одинарн' in x or 'одинар' in x:
                                    print('1')
                                    u = 1
                                    inter = 1
                        if u == 1:
                            break
                    
                    # for j in range(i, len(sent_list)):
                    #     if 'по' in sent_list[j].lower():
                    #         print(sent_list[j], sent_list[j+1])

    def get_literature(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            for style in self.__recognized_lit_templates:
                # if 'ГОСТ' in text:
                #     print(text, style, style in text)
                if style in text:

                    self.__requirements_of_literature['Temlate_name'] = style
                    print(style)
                    break
    
    def get_additional(self):
        mesures = ['больше', 'меньше', 'от', 'до','более', 'менее', 'превышал']
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            # Рисунки. Учитываем площадь, формат.
            
            
            if 'Рис' in text:
                n_text = ''
                for i, a in enumerate(text):
                    # if 
                    if i>0 and i<len(text)-2 and text[i] =='.':
                        # print(text[i-1], text[i+1])
                        
                        if text[i+2].islower():
                            n_text += '_'
                        else:
                            n_text += '.'
                    else:
                        n_text += a
                # print(n_text)
                list_of_sentences = n_text.split('.')
                # print(self.__recognized_formats)
                for format in self.__recognized_formats:
                    if format in text:
                        print(format)
                
                for j, sent in enumerate(list_of_sentences):
                    if 'размер' in sent.lower():
                        # print('РАЗМЕР')
                        nm = 0
                        regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                        x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                        sent_list = x.split(' ')
                        for k, word in enumerate(sent_list):
                            if 'размер' in word:
                                nm = k
                        # print(nm, sent_list)
                        op =0
                        for k in range(nm, len(sent_list)):
                                # print(sent_list[k])
                                if len(sent_list[k])>0:
                                    if sent_list[k][0].isdigit() and ('мм' in sent_list[k] or 'см' in sent_list[k]):
                                        print(sent_list[k])
                                        op = 1
                                    
                                    n = k
                                    t = k 
                                    
                                    while n>1 and op == 1:
                                        # print(sent_array[n])
                                        if sent_list[n].lower() in mesures:
                                            print(sent_list[n])
                                            n-=1
                                            
                                            break
                                        n-=1
                                    # print(sent_array[n])
                                    if 'не' in sent_list[n] and op ==1:
                                        print('не')
                                    while t < len(sent_list):
                                        if 'ширин' in sent_list[t]:
                                            print('ш')
                                        if 'выс' in sent_list[t]:
                                            print('в')
                                        t+=1
                    
                    if 'разрешение' in sent:
                        nm = 0
                        regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                        x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                        sent_list = x.split(' ')
                        for k, word in enumerate(sent_list):
                            if 'разреш' in word:
                                nm = k
                        # print(nm, sent_list)
                        for k in range(nm, len(sent_list)):
                                # print(sent_list[k])
                                if sent_list[k][0].isdigit():
                                    print(sent_list[k])

            if 'Таб' in text:
                for j, sent in enumerate(list_of_sentences):
                    if 'размер' in sent.lower():
                        # print('РАЗМЕР')
                        nm = 0
                        regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                        x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                        sent_list = x.split(' ')
                        for k, word in enumerate(sent_list):
                            if 'размер' in word:
                                nm = k
                        # print(nm, sent_list)
                        op =0
                        for k in range(nm, len(sent_list)):
                                # print(sent_list[k])
                                if len(sent_list[k])>0:
                                    if sent_list[k][0].isdigit() and ('мм' in sent_list[k] or 'см' in sent_list[k]):
                                        print(sent_list[k])
                                        op = 1
                                    
                                    n = k
                                    t = k 
                                    
                                    while n>1 and op == 1:
                                        # print(sent_array[n])
                                        if sent_list[n].lower() in mesures:
                                            print(sent_list[n])
                                            n-=1
                                            
                                            break
                                        n-=1
                                    # print(sent_array[n])
                                    if 'не' in sent_list[n] and op ==1:
                                        print('не')
                                    while t < len(sent_list):
                                        if 'ширин' in sent_list[t]:
                                            print('ш')
                                        if 'выс' in sent_list[t]:
                                            print('в')
                                        t+=1
                                  
    
    def get_values(self):
        fl = 0
        paragraphs = self.__get_all_paragraphs()
        mesures = ['больше', 'меньше', 'от', 'до','более', 'менее', 'превышал']
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            list_of_sentences = text.split('.')
            
            if 'ключевые слова' in text.lower():
                regex = re.compile("(\d )", re.S)
                for sent in list_of_sentences:
                    regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                    x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                    # print(x)
                    sent_array = x.lower().split(' ')
                    for j,word in enumerate(sent_array):
                        if len(word)> 0:
                            if word[0].isdigit() and j>0:
                                print(word)
                                n = j
                                while n>1:
                                    # print(sent_array[n])
                                    if sent_array[n].lower() in mesures:
                                        print(sent_array[n])
                                        n-=1
                                        break
                                    n-=1
                                # print(sent_array[n])
                                if 'не' in sent_array[n]:
                                    print('не')

            for j, sent in enumerate(list_of_sentences):
                regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                point = 0
                if 'объем' in x.lower() or 'объём' in x.lower() and ('статьи' in x.lower() or 'текст' in x.lower()):
                    sent_array = x.lower().split(' ')
                    # print('here')
                    for p, word in enumerate(sent_array):
                        if 'статьи' in word or 'текст' in word:
                            # print(p, word)
                            point = p
                    k = 0
                    for l, word in enumerate(sent_array):
                        # print(fl)
                        if  'объем' in word.lower() or 'объём' in word.lower():
                            k = 1
                        if len(word)>0:
                            if k == 1 and word[0].isdigit():
                                z = word
                                # не более не менее. простмотреть.
                                if 'знаков' in word or 'стр' in word:
                                    print(word)
                                    n = l
                                    while n>1:
                                        # print(sent_array[n])
                                        if sent_array[n].lower() in mesures:
                                            print(sent_array[n])
                                            n-=1
                                            break
                                        n-=1
                                    # print(sent_array[n])
                                    if 'не' in sent_array[n]:
                                        print('не')
                
            if 'список литературы' in text.lower() or 'списка литературы' in text.lower():
                # print('Р')
                regex = re.compile("(\d )", re.S)
                for sent in list_of_sentences:
                    regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                    x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                    # print(x)
                    sent_array = x.lower().split(' ')
                    for j,word in enumerate(sent_array):
                        if len(word)> 0:
                            if word[0].isdigit() and j>0 and word[-1].isalpha() and word[-2].isalpha():
                                print(word)
                                n = j
                                while n>1:
                                        # print(sent_array[n])
                                    if sent_array[n].lower() in mesures:
                                        print(sent_array[n])
                                        n-=1
                                        break
                                    n-=1
                                    # print(sent_array[n])
                                if 'не' in sent_array[n]:
                                    print('не')

            if 'рисунков' in text.lower():
                regex = re.compile("(\d )", re.S)
                for sent in list_of_sentences:
                    regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                    x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                    # print(x)
                    sent_array = x.lower().split(' ')
                    for j,word in enumerate(sent_array):
                        if len(word)> 0:
                            if word[0].isdigit() and j>0 and word[-1].isalpha() and word[-2].isalpha() and 'рис' in word:
                                print(word)
                                n = j
                                while n>1:
                                        # print(sent_array[n])
                                    if sent_array[n].lower() in mesures:
                                        print(sent_array[n])
                                        n-=1
                                        break
                                    n-=1
                                    # print(sent_array[n])
                                if 'не' in sent_array[n]:
                                    print('не')         

    def __get_data_of_style(self, text):
        list_of_sentences = text.split('.')
        inter = 0
        for i, sent in enumerate(list_of_sentences):
            regex = re.compile("(\d )", re.S)
            x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
            sent_list = x.split(' ')
            # print(sent_list)
            y = 'верхнее' in x.lower() or 'нижнее' in x.lower() or 'правое' in x.lower() or 'левое' in x.lower()
            if 'поля' in x.lower() or 'поле' in x.lower() and y:
                    # print(y)
                print('Поля')
                for i, elem in enumerate(sent_list):
                        # print(elem, elem.lower() == 'верхнее', elem.lower() == 'нижнее', elem.lower() == 'правое', elem.lower() == 'левое')
                    if elem.lower() == 'верхнее':
                        print('here')
                        for j in range(i, len(sent_list)):
                                # print(sent_list[j])
                            if sent_list[j][0].isdigit():
                                print(sent_list[j])
                                break
                    elif elem.lower() == 'нижнее':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                    elif elem.lower() == 'правое':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                    elif elem.lower() == 'левое':
                            for j in range(i, len(sent_list)):
                                if sent_list[j][0].isdigit():
                                    print(sent_list[j])
                                    break
                    elif y == False:
                            m =0
                            # print(sent_list)
                            for j, word in enumerate(sent_list):
                                if 'поле' in word.lower() or 'поля' in word.lower():
                                    m = j
                                if j> m and word[0].isdigit() and 'см' in word:
                                    print(word)
                                    break
                
            if 'отступ' in x.lower() and ('первой' in x.lower() or 'красной' in x.lower() or ('начал' in x.lower() and 'абзац' in x.lower())):
                    
                    for i, elem in enumerate(sent_list):
                        if 'отступ' in elem.lower():
                            flag = 0
                            flag2 = 0
                            for j in range(i, len(sent_list)):
                                # print(sent_list[j])
                                if 'абзац' in sent_list[j].lower():
                                    flag2 = 1
                                # print(flag2)
                                if 'первой' in sent_list[j] or 'красной' in sent_list[j]:
                                    flag = 1
                                # print(flag)
                                if sent_list[j][0].isdigit() and ('начал' in x.lower() and 'абзац' in x.lower()):
                                    print('Отступ красной строки')
                                    print(sent_list[j])
                                    break
                # print('Times New Roman' in x)
            elif 'отступ' in x.lower():
                    print('Отступ', x)
                    n = 'справа' in x.lower() or 'слева' in x.lower() or 'сверху' in x.lower() or 'снизу' in x.lower()
                    print(n)
                    if n:
                        for n, elem in enumerate(sent_list):
                            if 'отступ' in elem.lower():
                                for j in range(n, len(sent_list)):
                                    # print(sent_list[j]
                                    if 'справа' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'слева' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'сверху' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    elif 'снизу' in sent_list[j]:
                                        print('here')
                                        for l in range(j, len(sent_list)):
                                            # print(sent_list[j])
                                            if sent_list[l][0].isdigit():
                                                print(sent_list[l])
                                                break
                                    
                    else:
                        print(sent_list)
                        for i, elem in enumerate(sent_list):
                            if 'отступ' in elem.lower():
                                for j in range(i, len(sent_list)):
                                    # print(sent_list[j]
                                    if sent_list[j][0].isdigit():
                                        print(sent_list[j])
                                        break

            if 'интервал' in x.lower() and ('абзац' not in x.lower()) and inter == 0:
                    print('Межстрочный интервал')
                    print(sent_list)
                    for j, word in enumerate(sent_list):
                        
                        u = 0
                        if 'интервал' in word.lower():
                            # print(j, word)
                            t = j
                            fl = 0
                            while sent_list[t][-1]!=',':
                                
                                if sent_list[t][0].isdigit():
                                    fl =1
                                    u = 1
                                    print(sent_list[t])
                                    inter = 1
                                    break
                                t+=1
                                if t>=len(sent_list):
                                    break
                            
                            if fl == 0:
                                # print('here', 'одинарн' in x, x)
                                if 'полуторны' in x or 'полтора' in x:
                                    print('1,5')
                                    u = 1
                                    inter = 1
                                if 'одинарн' in x or 'одинар' in x:
                                    print('1')
                                    u = 1
                                    inter = 1
                                if 'двойн' in x:
                                    print('2')
                                    u = 1
                                    inter = 1
                                if 'строки' in sent:
                                    # print('руку', sent_list[j], sent_list)
                                    for k in range(j, len(sent_list)):
                                        if 'строки' in sent_list[k]:
                                            print(sent_list[k])
                        if u == 1:
                            break                               

            if 'выравнивание' in x.lower():
                    # print(fl, sent_list, i)
                    print('Выравнивание' , i)
                    l = 0
                    for j, word in enumerate(sent_list):
                        for k in range(j, len(sent_list)):
                            # print(sent_list[k])
                            if 'ширине' in sent_list[k]:
                                print('ширине')
                                l = 1
                                break
                            elif 'левому' in sent_list[k]:
                                print('левому краю')
                                l = 1
                                break
                            elif 'правому' in sent_list[k]:
                                print('правому краю')
                                l = 1
                                break
                            elif 'центру' in sent_list[k]:
                                print('центру')
                                l = 1
                                break
                        if l == 1:
                            break
            
            for font in self.__recognized_fonts:
                    if font in x:
                        print('Font')
                        print(font)
            for j, word in enumerate(sent_list):
                if 'шрифт' in x.lower() or 'кегль' in x.lower():
                    # print('herere')
                    for k in range(j, len(sent_list)):
                        if len(word)>0:
                            if sent_list[j][0].isdigit():
                                print('Кегль')
                                print(sent_list[k])
                                break
    
    def __get_data_of_lit(self, text: str):
        list_of_sentences = text.split('.')
        for style in self.__recognized_lit_templates:
                # if 'ГОСТ' in text:
                #     print(text, style, style in text)
                if style in text:
                    self.__requirements_of_literature['Temlate_name'] = style
                    print(style)
                    break

    def __get_data_of_additional(self, text: str):
        list_of_sentences = text.split('.')
        mesures = ['больше', 'меньше', 'от', 'до','более', 'менее', 'превышал']
        if 'рис' in text:
                n_text = ''
                for i, a in enumerate(text):
                    # if 
                    if i>0 and i<len(text)-2 and text[i] =='.':
                        # print(text[i-1], text[i+1])
                        
                        if text[i+2].islower():
                            n_text += '_'
                        else:
                            n_text += '.'
                    else:
                        n_text += a
                # print(n_text)
                list_of_sentences = n_text.split('.')
                # print(list_of_sentences)
                for format in self.__recognized_formats:
                    if format in text:
                        print(format)
                
                for j, sent in enumerate(list_of_sentences):
                    
                    regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                    x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                    sent_list = x.split(' ')
                    for word in sent_list:
                        if 'см' in word or 'мм' in word and len(word)>0:
                            if word[0].isdigit():
                                print(word)
                    
                    if 'разрешение' in sent:
                        nm = 0
                        regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                        x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                        sent_list = x.split(' ')
                        for k, word in enumerate(sent_list):
                            if 'разреш' in word:
                                nm = k
                        # print(nm, sent_list)
                        for k in range(nm, len(sent_list)):
                                # print(sent_list[k])
                                if sent_list[k][0].isdigit():
                                    print(sent_list[k])

        if 'аблиц' in text:
                n_text = ''
                for i, a in enumerate(text):
                    # if 
                    if i>0 and i<len(text)-2 and text[i] =='.':
                        # print(text[i-1], text[i+1])
                        
                        if text[i+2].islower():
                            n_text += '_'
                        else:
                            n_text += '.'
                    else:
                        n_text += a
                # print(n_text)
                list_of_sentences = n_text.split('.')
                # print(list_of_sentences)
                for format in self.__recognized_formats:
                    if format in text:
                        print(format)
                
                for j, sent in enumerate(list_of_sentences):
                    
                    regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                    x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                    sent_list = x.split(' ')
                    for word in sent_list:
                        if 'см' in word or 'мм' in word and len(word)>0:
                            if word[0].isdigit():
                                print(word)
                    
    def __get_data_of_value(self, text: str):
        list_of_sentences = text.split('.')
        mesures = ['больше', 'меньше', 'от', 'до','более', 'менее', 'превышал', 'превышать', 'должен']
        for j, sent in enumerate(list_of_sentences):
            if 'ключ' in sent.lower() and 'слов' in sent:
                regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                sent_list = x.split(' ')
                # От до проверить
                for i, word in enumerate(sent_list):
                    word = word.replace('(','')
                    word = word.replace(')','')
                    if len(word)>0:
                        if 'слов' in word and word[0].isdigit():
                            print(word)
                            k = i
                            n = i
                            f = 0
                            while n>1:
                            # print(sent_array[n])
                                for mesure in mesures:
                                    if mesure in sent_list[n].lower():
                                        f = 1
                                if f == 1:
                                    print(sent_list[n])
                                    n-=1
                                    break
                                else:
                                    break
                            n-=1
                                    # print(sent_array[n])
                            if 'не' in sent_list[n]:
                                print('не')
            elif 'слов' in sent or 'знак' in sent:
                regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                sent_list = x.split(' ')
                # От до проверить
                for i, word in enumerate(sent_list):
                    word = word.replace('(','')
                    word = word.replace(')','')
                    if len(word)>0:
                        if ('слов' in word or 'знак' in word) and word[0].isdigit():
                            print(word)
                            k = i
                            n = i-1
                            f = 0
                            while n>1:
                                # print(sent_list[n])
                                for mesure in mesures:
                                    if mesure in sent_list[n].lower():
                                        f = 1
                                if f == 1:
                                    print(sent_list[n])
                                    n-=1
                                    break
                                else:
                                    break
                            n-=1
                                    # print(sent_array[n])
                            if 'не' in sent_list[n]:
                                print('не')
            
            if 'страниц' in sent:
                regex = re.compile("(\d )", re.S)
                # x - объединено число в одно
                x = regex.sub(lambda x: x.group()[0].replace(" ", ""), sent)
                sent_list = x.split(' ')
                # От до проверить
                for i, word in enumerate(sent_list):
                    word = word.replace('(','')
                    word = word.replace(')','')
                    if len(word)>0:
                        if ('страниц' in word) and word[0].isdigit():
                            print(word)
                            k = i
                            n = i
                            f = 0
                            while n>1:
                            # print(sent_array[n])
                                for mesure in mesures:
                                    if mesure in sent_list[n].lower():
                                        f = 1
                                if f == 1:
                                    print(sent_list[n])
                                    n-=1
                                    break
                                else:
                                    break
                            n-=1
                                    # print(sent_array[n])
                            if 'не' in sent_list[n]:
                                print('не')
            





    def __clean_text(self, text: str):
        n_text = ''
        for i, a in enumerate(text):
            if i>0 and i<len(text)-1 and a=='.':
                if text[i-1].isdigit() and text[i+1].isdigit():
                    pass
                else:
                    n_text+=a
            else:
                n_text += a
                

    def data_getter(self, struct_elem, text):
        data_of_style = self.__get_data_of_style(text)
        data_of_add = self.__get_data_of_additional(text)
        data_of_val =self.__get_data_of_value(text)

    def get_parts_of_article(self):
        paragraphs = self.__get_all_paragraphs()
        count = 0
        text_of_part = ''
        dict_for_struct = {}
        default = ''
        for paragraph in paragraphs:
            text = self.__get_text_from_element(paragraph)
            list_of_sentences = text.split('.')
            for elem_of_structure in  self.__recognized_struct_elems:
                if elem_of_structure in text:
                    # if elem_of_structure in dict_for_struct:
                    #     dict_for_struct[elem_of_structure]+=text_of_part
                    # else:
                    #     dict_for_struct[elem_of_structure] = text_of_part
                    # if elem_of_structure == 'Автор':
                    #     print(text_of_part, 'Автор' in text_of_part, elem_of_structure in text, elem_of_structure =='Автор')
                    #     print(elem_of_structure)
                    # print(elem_of_structure, text)
                    
                    # print(elem_of_structure, default, text_of_part, count)
                    # if default == 'Графический материал':
                    #     print('HERERERE', text_of_part)
                    if default in dict_for_struct:
                        dict_for_struct[default] += ' '+ text_of_part
                    else:
                        dict_for_struct[default] = text_of_part
                    default = elem_of_structure
                    text_of_part = ''
                    count= 0
            # print(count)        
            count+=1
            text_of_part+= ' '+ text
        
        if '' in dict_for_struct:
            txt = dict_for_struct['']
            print(txt)
        # print(dict_for_struct)
        for key, value in dict_for_struct.items():
            if 'таблиц' == key:
                print(key, value)
        print(dict_for_struct.keys())
        # Получить для каждой части стать
        for key, value in dict_for_struct.items():
            if 'таблиц' == key:
                t = value.replace('\xa0',' ')
                # print(t)
                self.data_getter(key, t)



                            

    

                        




            















                

        
        

        

        