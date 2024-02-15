import zipfile
import lxml.etree as et
import os
import json
from content.read_the_file import Read_the_file

def file_opener():
    

        
        get_data = Read_the_file('doc1.docx')
        x = int(input())
        
        if x == 1:
            data = get_data.get_parts_of_article()
            data = get_data.set_default_values(data)
            # print(data)
            with open('out/out.json', 'w+', encoding='utf-8') as out:
                data['Вы имели ввиду?'] = ''
                json.dump(data, out, ensure_ascii=False)
                # out.write('Вы имели ввиду?\n')
                # gap = 0
        #         for key, value in data.items():
        #             # print('======')
        #             # print(key)
        #             out.write('\n======\n'+key)
        #             if type(value) == dict:
        #                 for key1, value1 in value.items():
        #                     # print(' ' + key1)
        #                     out.write('\n '+key1+'\n')
        #                     if type(value1) == str:
        #                         # print('  ' + str(value1))
        #                         out.write('\n  ' + str(value1)+'\n')
        #                     elif type(value1) == dict:
        #                         for key2, value2 in value1.items():
        #                             # print('  '+key2)
        #                             out.write('\n  ' + str(key2)+'\n')
        #                             if type(value2) == str:
        #                                 # print('   '+value2)
        #                                 out.write('\n   ' + str(value2)+'\n')
        #                             elif type(value2) == dict:
        #                                 for key3, value3 in value2.items():
        #                                     # print('   '+ key3, value3)
        #                                     out.write('\n   ' + str(key3)+' '+ str(value3) +'\n')
        #             elif type(value) == list:
        #                 # print(' '+ str(value))
        #                 out.write('\n '+str(value)+'\n')       
                    
        #             # print('======')
        elif x==2:
            data = get_data.get_parts_of_article_engl()
            data = get_data.set_default_values(data)
            # print(data)
            with open('out/out.json', 'w+', encoding='utf-8') as out:
                
                json.dump(data, out, ensure_ascii=False)