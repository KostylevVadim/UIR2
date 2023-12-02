
import lxml.etree as et
import re


class Read_the_file:
    __recognized_fonts=['Times New Roman',
                     'Calibri', 'Arial']
    __recognized_lit_templates = [
        'ГОСТ Р 7.0.100-2018',
        'ГОСТ Р 7.0.5–2008',
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
    __namespaces = {'w':"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lang = 'rus'
    
    def __init__(self, file):
        self.__etree = et.parse(file)
        self.__root =  self.__etree.getroot()
        self.__requirements_of_format ={
            'Format': None,
            'lang': None,
            'Numeration': None
        }
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
        self.__requirements_of_structure = {
            'title': '',
            'Author': '',
            'Annotation': '',
            'Contacts': ''
        }
        self.__requirements_of_literature = {
            'Temlate_name' : '',
            'Uses examples': []
        }
        self.__additional = {
            'tables': '',
            'pic': '',
            'formula':''
        }
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
        with open('result.txt', "w", encoding="utf-8") as file:
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
            pattern = r'a\d\+'
            text_arr = text.split(' ')
            for i, word in enumerate(text_arr):
                # print(word)
                if 'А4' in word:
                    print(word, re.fullmatch(pattern, word.lower()))
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
        elem = 0
        pic = 0
        form = 0
        tab = 0
        # text = 0
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            
            p1 = 'оформление рисунков'
            p2 = 'оформление иллюстраций'
            t1 = 'оформление таблиц'
            f1 = 'оформление формул'
            if 'элементов статьи' in text.lower() or ('рисунки:'in text.lower() or 'таблицы:' in text.lower() or 'формулы:' in text.lower()):
                elem = 1
            if ('рисун' in text.lower() or ('графическ' in text.lower() and 'библ' not in text.lower())):
                pic = 1
                self.__additional['pic'] += ' '+ text 
                # print('p', text, 'рисунк' in text.lower(), 'графическ' in text.lower())
                
            elif elem ==1:
                pic = 0
            
            if 'таблиц' in text.lower():
                tab = 1
                # print('t')
                self.__additional['tables'] += ' '+ text 
            elif elem ==1:
                tab = 0

            
            if 'формул' in text.lower():
                form = 1
                # print('f')
                self.__additional['formula'] += ' '+ text 
            elif elem ==1:
                form = 0
            print(elem, pic, form, tab)
            for font in self.__recognized_fonts:
                if font in text:
                    if tab+form+pic == 0 and self.__requirements_of_style['Font'] is None :
                        self.__requirements_of_style['Font'] = font
                    break
            if 'размер' in text.lower() and ('шрифта' in text.lower() or 'шрифт' in text.lower() or 'кегль:' in text.lower() or 'кегль' in text.lower() or 'кегля' in text.lower() or 'кегля:' in text.lower()):
                # print('hh')
                text_array = text.split(' ')
                # print(len(text_array))
                s = ''
                for i, word in enumerate(text_array):
                    if 'размер' in word.lower():
                        # print(word)
                        j = i
                        for x in range(j, len(text_array)):
                            # print(s)
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x] or ',' in text_array[x]:
                                break
                if tab+form+pic == 0 and self.__requirements_of_style['kegl'] is None:
                    self.__requirements_of_style['kegl'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
            
            field = 'поля' in text.lower() or ('размер' in text.lower() and 'полей' in text.lower())
            # print(field)
            if field:
                text_array = text.split(' ')
                
                s = ''
                for i, word in enumerate(text_array):
                    l = re.search(r'поля\D', " ".join(text_array[i:]))
                    if 'поля' in word.lower(): 
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                            # print(s)
                        break
                    elif 'размер' in  word.lower() and l is not None:
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                if tab+form+pic == 0 and self.__requirements_of_style['field'] is None:
                    self.__requirements_of_style['field'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
                
            ind = 'отступ' in text.lower() and ('абзацный' in text.lower() or 'абзаца' in text.lower()) and 'первой' not in text.lower()
            if ind:
                print('here')
                text_array = text.split(' ')
                
                s = ''
                for i, word in enumerate(text_array):
                    l = re.search(r'отступ\D', " ".join(text_array[i:]))
                    l1 = re.search(r'абзаца\D', " ".join(text_array[i:]))
                    
                    if 'отступ' in word.lower() and l1 is not None: 
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                    elif ('абзацный' in word.lower() or 'абзаца' in word.lower())and l is not None:
                        j = i
                        # print('here2')
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                
                if tab+form+pic == 0 and self.__requirements_of_style['indent'] is None:
                    self.__requirements_of_style['indent'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
                
            
            int_f = 'интервал' in text.lower() and ('междустрочный' in text.lower() or 'межстрочный' in text.lower() or
                                                    'между строками' in text.lower())
            if int_f:
                text_array = text.split(' ')
                s = ''
                for i, word in enumerate(text_array):
                    if 'интервал' in word.lower() and re.search(r'между строками', " ".join(text_array[i:])):
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                    elif (word.lower() == 'междустрочный' or word.lower() == 'межстрочный'):
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                if tab+form+pic == 0 and self.__requirements_of_style['interval_string'] is None:
                    self.__requirements_of_style['interval_string'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
                # self.__requirements_of_style['interval_string'] = s

            int_p = 'интервал' in text.lower() and ('между абзацами' in text.lower())
            if int_p:
                # print('here')
                text_array = text.split(' ')
                s = ''
                for i, word in enumerate(text_array):
                    # print(" ".join(text_array[i:]), re.search(r'между абзацами', " ".join(text_array[i:])) is not None, word == 'интервал')
                    if word.lower() == 'интервал' and re.search(r'между абзацами', " ".join(text_array[i:])) is not None:
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                if tab+form+pic == 0 and self.__requirements_of_style['interval_par'] is None:
                    self.__requirements_of_style['interval_par'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
                # self.__requirements_of_style['interval_par'] = s

            if 'выравнивание' in text.lower():
                text_array = text.split(' ')
                s = ''
                for i, word in enumerate(text_array):
                    if word.lower() == 'выравнивание':
                        j = i
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                
                if tab+form+pic == 0 and self.__requirements_of_style['jc'] is None:
                    self.__requirements_of_style['jc'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s
                # self.__requirements_of_style['jc'] = s
            if 'отступ' in text.lower() and ('первой строки' in text.lower() or 'красной строки' in text.lower() or 'красная строка' in text.lower()) :
                text_array = text.lower().split(' ')
                s = ''
                # print('tut')
                for i, word in enumerate(text_array):
                    f_s = re.search(r'первой строки', " ".join(text_array[i:])) is not None
                    k_s = re.search(r'красной строки', " ".join(text_array[i:])) is not None
                    f_s1 = re.search(r'первая строка', " ".join(text_array[i:])) is not None
                    k_s1 = re.search(r'красная строка', " ".join(text_array[i:])) is not None
                    if word.lower() == 'отступ' and (f_s or k_s or f_s1 or k_s1):
                        j = i
                        # print('zdes')
                        for x in range(j, len(text_array)):
                            s+= str(text_array[x])+ ' '
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                                break
                        break
                if tab+form+pic == 0 and self.__requirements_of_style['indent_first'] is None:
                    self.__requirements_of_style['indent_first'] = s
                # elif pic == 1:
                #     self.__additional['pic'] += s
                # elif tab == 1:
                #     self.__additional['tables'] +=s
                # elif form == 1:
                #     self.__additional['formula']+=s




        # print(self.__requirements_of_style)
        # print(self.__additional)
        
    

    def get_literature(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            for style in self.__recognized_lit_templates:
                if style in text:
                    self.__requirements_of_literature['Temlate_name'] = style
                    break
    
    def get_additional(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            s = ''
            table = 'таблицы' in text.lower() and ('название' in text.lower() or ('шрифт' in text.lower() or 'размер' in text.lower()) 
                                                   or 'номер' in text.lower() or 'интервал' in text.lower())
            pic = 'рисун' in text.lower() 
            formula = 'формул' in text.lower()
            s_all = ''
            if table:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    if 'интервал' in word.lower():
                        
                        s_inter = []
                        j_for = i
                        j_b = i-1
                        # print(word, j_for, j_b)
                        if j_b>=0:
                            # print(j_b)
                            while j_b >=0: 
                                if '.' not in text_array[j_b] and ';' not in text_array[j_b] and '\n' not in text_array[j_b] and ',' not in text_array[j_b]:
                                    s_inter.insert(0,text_array[j_b])
                                    j_b-=1
                                else: 
                                    break
                            # print(s_inter)
                        for x in range(j_for, len(text_array)):
                            if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x] or ',' in text_array[x]:
                                s_inter.append(text_array[x])
                                break
                            s_inter.append(text_array[x])
                        s1 = " ".join(s_inter)
                        # print(s1)
                        s_all += s1
                    j_temp = i
                    while '.' not in text_array[j_temp] and ';' not in text_array[j_temp] and '\n' not in text_array[j_temp]:
                        j_temp+=1
                    # print(i, j_temp, text_array[j_temp])
                    tables = re.search(r'таблицы', " ".join(text_array[i:j_temp])) is not None
                    
                    if 'размер' in word.lower() and tables:
                        s_inter = []
                        j_for = i
                        for x in range(j_for, len(text_array)):
                            s_inter.append(text_array[x])
                            # if '.' in text_array[x] or ';' in text_array[x] or '\n' in text_array[x]:
                            #     s_inter.append(text_array[x])
                            if x< len(text_array):
                                if text_array[x+1][0].isupper():
                                    break
                            
                        s2 = " ".join(s_inter)
                        s_all += s2
                        # print(s2)
                    
                    if 'название' in word.lower():
                        s_inter = []
                        j_for = i
                        for x in range(j_for, len(text_array)):
                            s_inter.append(text_array[x])
                            if x< len(text_array):
                                if text_array[x+1][0].isupper():
                                    break
                            
                        s3 = " ".join(s_inter)
                        s_all += s3
                        # print(s3)
                    
                    if 'нумеруются' in word.lower():
                        s_inter = []
                        j_for = i
                        for x in range(j_for, len(text_array)):
                            s_inter.append(text_array[x])
                            # print(x, len(text_array))
                            if x < len(text_array):
                                if text_array[x+1][0].isupper():
                                    break
                            
                        s4 = " ".join(s_inter)
                        s_all += s4
                        # print(s4)
                    
                    # Выравнивание, сдалеать дополнительные проверки на вхождение до.
                    # print(s_all)
                    if 'выравн' in word.lower():
                        if 'выравн' in s_all:
                            pass
                        else:
                            s_inter = []
                            j_for = i
                            for x in range(j_for, len(text_array)):
                                s_inter.append(text_array[x])
                                # print(x, len(text_array))
                                if x < len(text_array):
                                    if text_array[x+1][0].isupper():
                                        break
                                
                            s5 = " ".join(s_inter)
                            s_all += s5
                            # print(s5)

        # for i, paragraph in enumerate(paragraphs):
        #     text = self.__get_text_from_element(paragraph)
        #     s = ''
        #     pic = 'рисун' in text.lower()

    
    def get_values(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            s = ''
            pages = (('страниц' in text.lower() or 'символов'in text.lower() or 'знаков'in text.lower()) and 'количество' in text.lower()) or (('объём' in text.lower() or 'объем' in text.lower()) and ('статьи' in text.lower() or 'текста' in text.lower()))
            
            if pages:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    n = " ".join(text_array[i:])
                    print(n)
                    num = 0
                    for elem in n:
                        if elem.isdigit():
                            num=1
                    print(num)
                    if 'страниц' not in n and 'знаков' not in n and 'символов' not in n:
                        break
                    if 'количество' in word.lower():
                        # print(i)
                        
                        print('количество123')
                        # while text_array[j] == text_array[j].lower():
                        #     s+=text_array[j]+ ' '
                        #     j+=1
                        #     if j== len(text_array):
                        #         break
                        #     print(s)
                        
                        if num == 1:
                            self.__requirements_of_value['Min_number_of_pages'] = n
                            break
                        

                            
                                 
                        
                        
                    elif ('объём' in word.lower() or 'объем' in word.lower()) and num == 1:
                        # print(word, i)
                        #Две ситуации. Минимальный объем статьи : N, Объем статьи: от ... до ...
                        # Случай 1
                        print('количество456')
                        n = " ".join(text_array[i:])
                        self.__requirements_of_value['Min_number_of_pages'] = n
                        break
                        
            lit = (('ссылок' in text.lower() or 'источников'in text.lower()) and 'количество' in text.lower()) or (('объём' in text.lower() or 'объем' in text.lower()) and 'списка источников' in text.lower())
            if lit:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    n = " ".join(text_array[i:])
                    for elem in n:
                        if elem.isdigit():
                            num=1
                    if 'количество' in word.lower():
                        if 'ссылок' not in n.lower() and 'источников' not in n.lower():
                            break
                        if num == 1:
                            self.__requirements_of_value['Min_lit_number'] = n
                            break

                        


                    elif ('объём' in word.lower() or 'объем' in word.lower()) and 'списка источников' in n.lower() and num == 1:
                        n = " ".join(text_array[i:])
                        # print(word)
                        if 'списка источников' not in n:
                            break
                        self.__requirements_of_value['Min_lit_number'] = n
                        break
                        
            pic = (('картинок' in text.lower() or 'иллюстраций'in text.lower() or 'изображений' in text.lower()) and 'количество' in text.lower())
            if pic:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    n = " ".join(text_array[i:])
                    for elem in n:
                        if elem.isdigit():
                            num=1
                    if 'количество' in word.lower():
                        if 'рисунков' not in n.lower() and 'картинок' not in n.lower() and 'изображений' not in n.lower():
                            break
                        if num == 1:
                            self.__requirements_of_value['Pic_number'] = n
                            break

            tab = (('таблиц' in text.lower()) and 'количество' in text.lower())
            if tab:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    n = " ".join(text_array[i:])
                    for elem in n:
                        if elem.isdigit():
                            num=1
                    if 'количество' in word.lower():
                        if 'таблиц' not in n.lower() :
                            break
                        if num == 1:
                            self.__requirements_of_value['Tab_number'] = n
                            break
            key_words =   (('ключевых слов' in text.lower()) and 'количество' in text.lower())
            if key_words:
                text_array = re.split(r'\s', text)
                # print(text_array)
                for i, word in enumerate(text_array):
                    n = " ".join(text_array[i:])
                    for elem in n:
                        if elem.isdigit():
                            num=1
                    if 'количество' in word.lower():
                        if 'ключевых слов' not in n.lower() :
                            break
                        if num == 1:
                            self.__requirements_of_value['Key_word_num'] = n
                            break
        # print(self.__requirements_of_value)
    

    def get_structure(self):
        paragraphs = self.__get_all_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            text = self.__get_text_from_element(paragraph)
            if 'название' in text.lower():
                
                text_array = re.split(r'\s', text)
                # print(text_array)
                if len(text_array) <= 2:
                    j = i+1
                    # print('here')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'название' in after.lower() and 'статьи' in after.lower():
                        j+=1
                        self.__requirements_of_structure['title'] += ' ' + after
                        after = self.__get_text_from_element(paragraphs[j])
                    
                elif self.__requirements_of_structure['title'] == '' :
                    j = i
                    # print('here1')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'название статьи.' in after.lower():
                        j+=1
                        self.__requirements_of_structure['title'] += ' ' + after
                        after = self.__get_text_from_element(paragraphs[j])
                    
            if 'автор' in text.lower():
                text_array = re.split(r'\s', text)
                # print(text_array)
                if len(text_array) <= 6:
                    j = i+1
                    # print('here')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'автор' in after.lower() or ('имя' in after.lower() or 'фамилия' in after.lower() or 'отчество' in after.lower()) or ('место' in after.lower() or 'организация' in after.lower()):
                        j+=1
                        self.__requirements_of_structure['Author'] += ' ' + after
                        after = self.__get_text_from_element(paragraphs[j])
                    
                elif self.__requirements_of_structure['Author'] == '':
                    j = i
                    # print('here1')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'автор' in after.lower() or ('имя' in after.lower() or 'фамилия' in after.lower() or 'отчество' in after.lower()) or ('место' in after.lower() or 'организация' in after.lower()):
                        j+=1
                        self.__requirements_of_structure['Author'] += ' ' + after
                        if j<len(paragraphs):
                            after = self.__get_text_from_element(paragraphs[j])
                        else:
                            break

            if 'аннотаци' in text.lower():
                text_array = re.split(r'\s', text)
                # print(text_array)
                if len(text_array) <= 2:
                    j = i+1
                    # print('here')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'аннотаци' in after.lower():
                        j+=1
                        self.__requirements_of_structure['Annotation'] += ' ' + after
                        if j<len(paragraphs):
                            after = self.__get_text_from_element(paragraphs[j])
                        else:
                            break
                    
                elif self.__requirements_of_structure['Annotation'] == '' :
                    j = i
                    # print('here1')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'аннотаци' in after.lower():
                        j+=1
                        self.__requirements_of_structure['Annotation'] += ' ' + after
                        if j<len(paragraphs):
                            after = self.__get_text_from_element(paragraphs[j])
                        else:
                            break

            if 'контакн' in text.lower():
                text_array = re.split(r'\s', text)
                # print(text_array)
                if len(text_array) <= 2:
                    j = i+1
                    # print('here')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'почта' in after.lower() and 'телефон' in after.lower():
                        j+=1
                        self.__requirements_of_structure['title'] += ' ' + after
                        if j<len(paragraphs):
                            after = self.__get_text_from_element(paragraphs[j])
                        else:
                            break
                    
                elif self.__requirements_of_structure['title'] == '' :
                    j = i
                    # print('here1')
                    after = self.__get_text_from_element(paragraphs[j])
                    while 'почта' in after.lower() and 'телефон' in after.lower():
                        j+=1
                        self.__requirements_of_structure['title'] += ' ' + after
                        if j<len(paragraphs):
                            after = self.__get_text_from_element(paragraphs[j])
                        else:
                            break

            

        # print(self.__requirements_of_structure)

                        
                        




            















                

        
        

        

        