
class Work_on_file:
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
                print(el)
                if 'w:rFonts' not in el:
                    result.write('<w:rFonts w:asciiTheme="majorBidi" w:eastAsia="Times New Roman" w:hAnsiTheme="majorBidi" w:cstheme="majorBidi"/>')

            result.write(el)
        return result
