from abc import ABC, abstractstaticmethod
import xml.etree.ElementTree as ET
import lxml.etree as et
import re
from iwork_on_file import Iwork_on_file
    
##Пока не учел что текст в таблицах может требовать свои фигулины в межстрочном интервале.
##Переделать таймс нью роман
##Переделать особое frst line space для тех что с отступом

class Work_on_file(Iwork_on_file):
    __namespaces = {'w':"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    @staticmethod
    def __find_Properties(paragraph):
        par_prop = paragraph.findall('.//w:pPr', Work_on_file.__namespaces)
        return par_prop[0]

    @staticmethod
    def __find_ind(paragraph):
        ind = paragraph.findall('.//w:ind', Work_on_file.__namespaces)
        if len(ind)>0:
            return ind[0]
        else:
            return None
    
    @staticmethod
    def __find_spacing(paragraph_propetries):
        spacing = paragraph_propetries.findall('.//w:spacing', Work_on_file.__namespaces)
        # print(spacing)
        if len(spacing)>0:
            return spacing[0]
        else:
            return None

    @staticmethod
    def __set_justification_for_pic(paragraph_after_pic):
        pic_templ = r'Рис [+]?\d+. '
        text = paragraph_after_pic.findall('.//w:t',Work_on_file.__namespaces)
        prop = Work_on_file.__find_Properties(paragraph_after_pic)
        txt = Work_on_file.__get_text_from_element(paragraph_after_pic)
        # for part in text:
        #     txt+=part.text
        # print(txt)
        if len(re.findall(pic_templ,txt)) == 0:
            raise Exception('NO Picture name after the picture')
        else:
            drawings = paragraph_after_pic.findall('.//w:drawing',Work_on_file.__namespaces)
            justification = paragraph_after_pic.findall('.//w:jc',Work_on_file.__namespaces)
            if len(justification)>0:
                for el in justification:
                    el.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = 'center'
            else:
                par_prop = paragraph_after_pic.findall('.//w:pPr',Work_on_file.__namespaces)
                added = et.SubElement(par_prop[0],"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc",
                                       {"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val": "center"})
           
    @staticmethod
    def __get_text_from_element(element):
        text = element.findall('.//w:t',Work_on_file.__namespaces)
        txt = ''
        for part in text:
            txt+=part.text
        return txt 


    @staticmethod
    def __set_just(root):
        
        elements = root.findall('.//w:p',Work_on_file.__namespaces)
        flag_drawing_was_before = 0
        for i, element in enumerate(elements):
            drawings = element.findall('.//w:drawing',Work_on_file.__namespaces)
            justification = element.findall('.//w:jc',Work_on_file.__namespaces)
            if flag_drawing_was_before == 0 and len(drawings) ==0:
                if len(justification)>0:
                    for el in justification:
                        el.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = 'both'
                else:
                    par_prop = element.findall('.//w:pPr',Work_on_file.__namespaces)
                    added = et.SubElement(par_prop[0],"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc",
                                       {"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val": "both"})
            elif len(drawings) >0:
                flag_drawing_was_before = 1
                if len(justification)>0:
                    for el in justification:
                        el.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = 'center'
                else:
                    par_prop = element.findall('.//w:pPr',Work_on_file.__namespaces)
                    added = et.SubElement(par_prop[0],"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc",
                                       {"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val": "center"})
            elif flag_drawing_was_before == 1 and len(drawings) ==0:
                Work_on_file.__set_justification_for_pic(element)
                flag_drawing_was_before = 0


            
        return elements

    @staticmethod
    def __set_lines(root):
        
        elements = root.findall('.//w:p',Work_on_file.__namespaces)
        for element in elements:
            props = Work_on_file.__find_Properties(element)
            spacing = Work_on_file.__find_spacing(props)
            
            if spacing is not None:
                spacing.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line"] = '360'
            else:
                added = et.SubElement(props, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing", {
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line": '360'
                })
                

        return elements

    @staticmethod
    def __set_after_before(root):
        elements = root.findall('.//w:p',Work_on_file.__namespaces)
        for element in elements:
            props = Work_on_file.__find_Properties(element)
            spacing = Work_on_file.__find_spacing(props)
            spacing.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}after"] = '0'
            spacing.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}before"] = '0'
            spacing.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}beforeAutospacing"] =  "0"
            spacing.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}afterAutospacing"] =  "0"

    @staticmethod
    def __find_rPr(paragraph):
        par_prop = paragraph.findall('.//w:rPr', Work_on_file.__namespaces)
        if len(par_prop)>0:
            return par_prop[0]
        else:
            return None


    @staticmethod
    def set_justification(file, result):
        etree = et.parse(file)
        root =  etree.getroot()
        # print(root.tag, root.attrib)
        # Work_on_file.__find_pictures(root)
        elements = Work_on_file.__set_just(root)
        s = et.tounicode(etree)
        result.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+str(s))
        return result
    
    @staticmethod
    def set_Times_new_roman_everywhere(file, result):

        in_body = 0
        array= []
        for line in file:
            x = line.split('<')
            array +=x
        in_body = 0
        for i,el in enumerate(array):
            if len(el)>0:
                el = '<'+el
            if '<w:body>' in el:
                in_body = 1
            if '</w:body>' in el:
                in_body = 0
            if 'w:rFonts' in el and in_body == 1:
                el = '<w:rFonts w:asciiTheme="majorBidi" w:eastAsia="Times New Roman" w:hAnsiTheme="majorBidi" w:cstheme="majorBidi"/>'
            if in_body == 1 and 'w:rPr' in array[i-1]:
                
                if 'w:rFonts' not in el:
                    result.write('<w:rFonts w:asciiTheme="majorBidi" w:eastAsia="Times New Roman" w:hAnsiTheme="majorBidi" w:cstheme="majorBidi"/>')

            result.write(el)
        return result
    

    @staticmethod
    def set_first_linespace(file, result):
        etree = et.parse(file)
        root =  etree.getroot()
        elements = root.findall('.//w:p',Work_on_file.__namespaces)
        for element in elements:
            props = Work_on_file.__find_Properties(element)
            ind = Work_on_file.__find_ind(props)
            if ind is None:
                print(props)
                et.SubElement(props,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind", {
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLine':'709'
                })
            else:
                ind.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLine"] = '709'
            props = Work_on_file.__find_Properties(element)
            ind = Work_on_file.__find_ind(props)
            # print(ind.attrib)
        s = et.tounicode(etree)
        result.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+str(s))
        return result
     
    

    @staticmethod
    def set_spacing(file, result):
        etree = et.parse(file)
        root =  etree.getroot()
        elements = Work_on_file.__set_lines(root)
        elements = Work_on_file.__set_after_before(root)
        s = et.tounicode(etree)
        result.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+str(s))
        return result
    
    @staticmethod
    def __change_size_of_sections(root, list_sections, name_of_text):
        paragraphs = root.findall('.//w:p',Work_on_file.__namespaces)
        for paragraph in paragraphs:
            # text = paragraph.findall('.//w:t',Work_on_file.__namespaces)
            prop = Work_on_file.__find_Properties(paragraph)
            r = paragraph.findall('.//w:r',Work_on_file.__namespaces)
            rpr = Work_on_file.__find_rPr(prop)
            if len(r)>0:
                rpr = Work_on_file.__find_rPr(r[0])
            txt = Work_on_file.__get_text_from_element(paragraph)
            # for part in text:
            #     txt+=part.text
            for name in list_sections:
                if txt in name and txt not in name_of_text:
                    sz = prop.findall('.//w:sz', Work_on_file.__namespaces)
                    szCs = prop.findall('.//w:szCs', Work_on_file.__namespaces)
                    # print(sz)
                    if len(sz)>0 and len(szCs)>0:
                        x = sz[0]
                        y = szCs[0]
                        # print(x.attrib, y.attrib)
                        x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '26'
                        
                        y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '26'
                    else:
                        et.SubElement(prop,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                        et.SubElement(prop,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                    # for elem in rpr:
                    #     print(elem.tag, elem.attrib)    
                    sz = rpr.findall('.//w:sz', Work_on_file.__namespaces)
                    szCs = rpr.findall('.//w:szCs', Work_on_file.__namespaces)
                    if len(sz)>0 and len(szCs)>0:
                        x = sz[0]
                        y = szCs[0]
                        # print(x.attrib, y.attrib)
                        x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '26'
                        
                        y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '26'
                    else:
                        et.SubElement(rpr,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                        et.SubElement(rpr,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                elif txt not in name_of_text:
                    sz = prop.findall('.//w:sz', Work_on_file.__namespaces)
                    szCs = prop.findall('.//w:szCs', Work_on_file.__namespaces)
                    # print(sz)
                    if len(sz)>0 and len(szCs)>0:
                        x = sz[0]
                        y = szCs[0]
                        # print(x.attrib, y.attrib)
                        x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '24'
                        
                        y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '24'
                    else:
                        et.SubElement(prop,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                        et.SubElement(prop,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                    # for elem in rpr:
                    #     print(elem.tag, elem.attrib)
                    # 
                    sz = []
                    szCs = []
                    if rpr is not None:    
                        sz = rpr.findall('.//w:sz', Work_on_file.__namespaces)
                        szCs = rpr.findall('.//w:szCs', Work_on_file.__namespaces)
                    if len(sz)>0 and len(szCs)>0:
                        x = sz[0]
                        y = szCs[0]
                        # print(x.attrib, y.attrib)
                        x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '24'
                        
                        y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '24'
                    elif rpr is not None:
                        et.SubElement(rpr,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })
                        et.SubElement(rpr,"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs",{
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val":'26'
                        })


    @staticmethod
    def __chage_size_of_name(root, name_of_text):
        
        paragraphs = root.findall('.//w:p',Work_on_file.__namespaces)
        for paragraph in paragraphs:
            text = paragraph.findall('.//w:t',Work_on_file.__namespaces)
            prop = Work_on_file.__find_Properties(paragraph)
            r = paragraph.findall('.//w:r',Work_on_file.__namespaces)
            rpr = Work_on_file.__find_rPr(prop)
            if len(r)>0:
                rpr = Work_on_file.__find_rPr(r[0])
            txt = Work_on_file.__get_text_from_element(paragraph)
            # for part in text:
            #     txt+=part.text
            # print(txt==name_of_text)
            if txt in name_of_text:
                sz = prop.findall('.//w:sz', Work_on_file.__namespaces)
                szCs = prop.findall('.//w:szCs', Work_on_file.__namespaces)
                # print(sz)
                if len(sz)>0 and len(szCs)>0:
                    x = sz[0]
                    y = szCs[0]
                    # print(x.attrib, y.attrib)
                    x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '30'
                    
                    y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '30'
                # for elem in rpr:
                #     print(elem.tag, elem.attrib)    
                sz = rpr.findall('.//w:sz', Work_on_file.__namespaces)
                szCs = rpr.findall('.//w:szCs', Work_on_file.__namespaces)
                if len(sz)>0 and len(szCs)>0:
                    x = sz[0]
                    y = szCs[0]
                    # print(x.attrib, y.attrib)
                    x.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '28'
                    
                    y.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"] = '28'
                    
            
        return 'Done'
    
    

    # @staticmethod
    # def change_size_of_letters(file, result, list_of_names_of_sections, name_of_article):
    #     etree = et.parse(file)
    #     root =  etree.getroot()
    #     elements = Work_on_file.__chage_size_of_name(root,name_of_article)
    #     elements = Work_on_file.__change_size_of_sections(root, list_of_names_of_sections, name_of_article)
        
    #     s = et.tounicode(etree)
        
    #     result.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+str(s))
    #     return result
    

