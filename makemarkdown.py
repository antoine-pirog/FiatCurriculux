from structure import CVmaker
import re

class CVmakerMarkdown(CVmaker):
    def _postprocessors(self):
        self.text = re.sub(r"(hal-\d{8})", r"[\g<1>](https://hal.science/\g<1>)", self.text)
        self.text = re.sub(r"(10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+)", r"[\g<1>](https://dx.doi.org/\g<1>)", self.text) # Per Crossref's recommendation - modified
    ###################
    # HEADER
    ###################
    def _gen_header(self, header_dict):
        text = ""
        text += self._gen_fullname(header_dict) + "\n"*2
        text += self._gen_cvtitle(header_dict) + "\n"*2
        text += self._gen_contactinfo(header_dict) + "\n"*2
        text += "---" + "\n"*2
        return text
    def _gen_fullname(self, header_dict):
        return f"# {self._gen_firstname(header_dict)} **{self._gen_lastname(header_dict)}**"
    def _gen_cvtitle(self, header_dict):
        return f"**{header_dict['title']}**"
    def _gen_email(self, header_dict):
        return f"[{header_dict['e-mail']}](mailto:{header_dict['e-mail']})" 
    def _gen_phonenbr(self, header_dict):
        return header_dict["phone_number"]
    def _gen_github(self, header_dict):
        return f"Github: [{header_dict['github']}](https://github.com/{header_dict['github']})"
    def _gen_orcid(self, header_dict):
        return f"Orcid: [{header_dict['orcid']}](https://orcid.org/{header_dict['orcid']})"
    ###################
    # SECTIONS
    ###################
    def _gen_sections(self, sections_list):
        # Big CV sections (Education, Experience, Etc.)
        text = ""
        for section_dict in sections_list:
            text += self._gen_section(section_dict) + "\n"*2
        return text
    def _gen_section(self, section_dict):
        text = ""
        text += self._gen_section_title(section_dict) + "\n"*2
        for item_dict in section_dict["items"]:
            text += self._gen_cvitem(item_dict) + "\n"*2
        return text
    def _gen_section_title(self, section_dict):
        return f"## {section_dict['title'].upper()}"
    ###################
    # CV ITEMS
    ###################
    def _gen_cvitem(self, item_dict):
        title = self._gen_cvitem_title(item_dict)
        place = self._gen_place(item_dict)
        descr = self._gen_descr(item_dict)
        list_ = self._gen_list (item_dict)
        table = self._gen_table(item_dict)

        text = ""
        text += title + "\n"*2
        for field in [place, descr, list_, table]:
            if field.strip():
                text += field + "\n"*2
        text += "---" + "\n"*2
        return text
    def _gen_cvitem_title(self, item_dict):
        title = item_dict.get('title', '')
        date  = item_dict.get('date', '')
        fields = [title, date]
        formatted_title = " | ".join([x for x in fields if x.strip()])
        return f"### {formatted_title}"
    def _gen_place(self, item_dict):
        if "place" in item_dict:
            return f"*{item_dict['place']}*"
        return ""
    def _gen_descr(self, item_dict):
        if "descr" in item_dict:
            return f"{item_dict['descr']}"
        return ""
    def _gen_list(self, item_dict):
        if "list" in item_dict:
            text = ""
            for item in item_dict['list']:
                text += "- " + item + "\n"
            return text
        return ""
    def _gen_table(self, item_dict):
        if "table" not in item_dict:
            return ""
        table = item_dict["table"]
        text = ""
        keys = table[0]
        values = table[1:]
        text += f"|{'|'.join(keys)}|\n"
        text += f"|{'|'.join(['-' for _ in keys])}|\n"
        for row in values:
            row_text = f"|{'|'.join([str(x) for x in row])}|".replace("\n", "<br>")
            text += f"{row_text}\n"
        return text
    

CV = CVmakerMarkdown(
    input_file = "./cv_contents.json",
    output_file = "CV.md"
)
CV.make()