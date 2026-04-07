from abc import ABC
import json

class CVmaker(ABC):
    def __init__(self, input_file, output_file, encoding="utf-8"):
        """ Constructor """
        self.input_file = input_file
        self.output_file = output_file
        self.encoding = encoding
        with open(self.input_file, "r", encoding=self.encoding) as f:
            self.contents = json.load(f)
        self.separators = {
            "contact_info" : " | "
        }
    def make(self):
        """ Makes CV and writes to output file """
        self.text = ""
        self._preprocessors()
        self.text += self._gen_header(self.contents["header"])
        self.text += self._gen_sections(self.contents["sections"])
        self._postprocessors()
        with open(self.output_file, "w", encoding=self.encoding) as f:
            f.write(self.text)
    def _preprocessors(self):
        """ Processing to run on output text BEFORE writing CV
        
        For example, processing may be done on self.text 
        to append text before CV elements (e.g., header, formatting options)
        """
        return

    def _postprocessors(self):
        """ Processing to run on output text AFTER writing CV
        
        For example, processing may be done on self.text 
        to append text after CV elements (e.g., footer, formatting options)
        """
        return
    def _append_line(self, line):
        """ Helper function to add a line to buffered text """
        self.text += line + "\n"

    ###################
    # HEADER
    ###################
    def _gen_header(self, header_dict):
        """ Generates CV header (Name + title + information) - returns generated text """
        text = ""
        text += self._gen_fullname(header_dict) + "\n"
        text += self._gen_cvtitle(header_dict) + "\n"
        text += self._gen_contactinfo(header_dict) + "\n"
        return text
    def _gen_fullname(self, header_dict):
        """ Generate full name to write on CV header - returns generated text """
        return f"{self._gen_firstname(header_dict)} {self._gen_lastname(header_dict)}"
    def _gen_firstname(self, header_dict):
        """ Generate first name to write on CV header - returns generated text """
        return header_dict["first_name"]
    def _gen_lastname(self, header_dict):
        """ Generate last name to write on CV header - returns generated text """
        return header_dict["last_name"]
    def _gen_cvtitle(self, header_dict):
        """ Generate title to write on CV header - returns generated text """
        return header_dict["title"]
    def _gen_contactinfo(self, header_dict):
        """ Generate contact info to write on CV header - returns generated text """
        contact_info = [
            self._gen_email(header_dict),
            self._gen_phonenbr(header_dict),
            self._gen_github(header_dict),
            self._gen_orcid(header_dict)
        ]
        return self.separators["contact_info"].join([c for c in contact_info if c])
    def _gen_email(self, header_dict):
        """ Generate contact e-mail to write on CV header - returns generated text """
        return header_dict["e-mail"]
    def _gen_phonenbr(self, header_dict):
        """ Generate contact phone nbr to write on CV header - returns generated text """
        return header_dict["phone_number"]
    def _gen_github(self, header_dict):
        """ Generate Github Link to write on CV header - returns generated text """
        return header_dict["github"]
    def _gen_orcid(self, header_dict):
        """ Generate Orcid ID to write on CV header - returns generated text """
        return header_dict["orcid"]
    ###################
    # SECTIONS
    ###################
    def _gen_sections(self, sections_list):
        """ Generate Main CV sections (Education, Experience, Etc.) - returns generated text"""
        text = ""
        for section_dict in sections_list:
            text += self._gen_section(section_dict) + "\n"
        return text
    def _gen_section(self, section_dict):
        """ Generate section contents - returns generated text """
        text = ""
        text += self._gen_section_title(section_dict) + "\n"
        for item_dict in section_dict["items"]:
            text += self._gen_cvitem(item_dict) + "\n"
        return text
    def _gen_section_title(self, section_dict):
        """ Generate section title - returns generated text"""
        return f"{section_dict['title'].upper()}"
    ###################
    # CV ITEMS
    ###################
    def _gen_cvitem(self, item_dict):
        """ Generate CV item (title + date + location + contents [text/list/table in that order]) - returns generated text """
        title = self._gen_cvitem_title(item_dict)
        place = self._gen_place(item_dict)
        descr = self._gen_descr(item_dict)
        list_ = self._gen_list(item_dict)
        table = self._gen_table(item_dict)

        text = ""
        text += title + "\n"
        for field in [place, descr, list_, table]:
            if field.strip():
                text += field + "\n"
        return text
    def _gen_cvitem_title(self, item_dict):
        """ Generate CV item title line - returns generated text"""
        return f"{item_dict.get('title', '')} ({item_dict['date']})"
    def _gen_place(self, item_dict):
        """ Generate CV item location/structure - returns generated text """
        return f"{item_dict.get('place', '')}"
    def _gen_descr(self, item_dict):
        """ Generate CV item description text - returns generated text """
        return f"{item_dict.get('descr', '')}"
    def _gen_list(self, item_dict):
        """ Generate CV item description list - returns generated text """
        return f"{item_dict.get('list', '')}"
    def _gen_table(self, item_dict):
        """ Generate CV item description table - returns generated text """
        return ""
    
