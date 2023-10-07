from abc import ABC, abstractstaticmethod
import xml.etree.ElementTree as ET
class Iwork_on_file(ABC):
    @abstractstaticmethod
    def set_Times_new_roman_everywhere(file, result):
        pass
    @abstractstaticmethod
    def set_linespace_before_and_after(file, result):
        pass
    @abstractstaticmethod
    def set_first_linespace(file, result):
        pass
    @abstractstaticmethod
    def set_justification(file, result):
        pass


class Work_on_file(Iwork_on_file):
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
    def set_linespace_before_and_after(file, result):
        pass
    @staticmethod
    def set_first_linespace(file, result):
        pass
    
    @staticmethod
    def __get_body(root):
        s = ''
        y = None
        z = None
        body = None
        for child in root:
            dict_for_attr = child.attrib
            for key, value in dict_for_attr.items():
                if '/word/document.xml' in value:
                    x = child
                    for child_x in x:
                        print(child_x.tag, child_x.attrib)
                        # s+='Tag: '+ str(child_x.tag) + ' Attrib: '+ str(child_x.attrib)+ '\n'
                        y = child_x
        for child in y:
            z = child
        for child in z:
            body = child
        
        return body
        
    @staticmethod
    def __get_pPr(paragraph):
        s = ''
        for child in paragraph:
            if 'pPr' in str(child.tag):
                return child

    @staticmethod
    def __change_ns2_to_w(file, result):
        in_body = 0
        array= []
        for line in file:
            x = line.split('<')
            array +=x
        in_body = 0
        for i,el in enumerate(array):
            if len(el)>0:
                el = '<'+el
                print(el)
                if 'ns' in el:
                    s = ''
                    j = 1
                    while el[j]!=':':
                        s+=el[j]
                        j+=1
                    
                    print(s)

            result.write(el)
        return result



    @staticmethod
    def __set_pPr_js(paragraph_property):
        js_child = None
        for child in paragraph_property:
            print(child.tag)
            if 'jc' in str(child.tag):
                js_child = child
                key = list(js_child.attrib.keys())
                js_child.attrib[key[0]] = 'both'
        for child in paragraph_property:
            #print(child.tag)
            if 'jc' in str(child.tag):
                js_child = child
                key = list(js_child.attrib.keys())
                print(js_child.attrib[key[0]])
        print('///')
        

    @staticmethod
    def set_justification(file, result):
        et = ET.parse(file)
        root = et.getroot()
        s= ''
        body = Work_on_file.__get_body(root)
        for child in body:
            s+='Tag: '+ str(child.tag) + ' Attrib: '+ str(child.attrib)+ '\n'
            pPr = Work_on_file.__get_pPr(child)
            if pPr is not None:
                Work_on_file.__set_pPr_js(pPr)

        result.write(s)
        
        et.write('result.xml')
        f1 = open('result.xml', 'r+',encoding='utf-8')
        f2 = open('result2.xml', 'w+',encoding='utf-8')
        f2 = Work_on_file.__change_ns2_to_w(f1, f2)
        f2.close

                    
            
            
        return result