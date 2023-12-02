from abc import ABC, abstractstaticmethod
class Iwork_on_file(ABC):
    @abstractstaticmethod
    def set_Times_new_roman_everywhere(file, result):
        pass
    @abstractstaticmethod
    def set_spacing(file, result):
        pass
    @abstractstaticmethod
    def set_first_linespace(file, result):
        pass
    @abstractstaticmethod
    def set_justification(file, result):
        pass
    @abstractstaticmethod
    def change_size_of_letters(file, result, list_of_names_of_sections, name_of_article):
        pass