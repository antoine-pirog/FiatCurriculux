from structure import CVmaker
import re

TABLE_AMPERSAND_PLACEHOLDER = "<TABLE_AMPERSAND_PLACEHOLDER>"

###################
# UTILS
###################
def make_link(url, text):
    return r"\\href{%s}{%s}" % (url, text)
def make_bold(text):
    return r"\\textbf{%s}" % (text)
def make_italic(text):
    return r"\\textit{%s}" % (text)

class CVmakerLatex(CVmaker):
    def __init__(self, input_file, output_file, encoding="utf-8"):
        super().__init__(input_file, output_file, encoding)
        self.separators["contact_info"] =  "~$\\vert$~"
    def _preprocessors(self):
        with open("templates/latex_header.tex", "r") as f:
            self.text += f.read()
    def _postprocessors(self):
        if True:
            self.text = re.sub(r"\*\*([^ ].+?[^ ])\*\*", make_bold(r"\g<1>"), self.text)
            self.text = re.sub(r"\*([^ ].+?[^ ])\*", make_italic(r"\g<1>"), self.text)
            self.text = re.sub(r"(hal-\d{8})", make_link(url=r"https://hal.science/\g<1>", text=r"\g<1>"), self.text)
            self.text = re.sub(r"(10\.\d{4,9}\/[-._;()\/:a-zA-Z0-9]+)", make_link(url=r"https://dx.doi.org/\g<1>", text=r"\g<1>"), self.text) # Per Crossref's recommendation
        # todo : handle utf-8 characters cleanly ...
        char_table = {
            " & " : r" \& ",
            "α" : "$\\alpha$",
            "β" : "$\\beta$",
            "«" : '"',
            "»" : '"',
        }
        for c in char_table:
            self.text = self.text.replace(c, char_table[c])
        self.text = self.text.replace(TABLE_AMPERSAND_PLACEHOLDER, " & ")
        
        with open("templates/latex_footer.tex", "r") as f:
            self.text += f.read()
        self.text += "\n"
    ###################
    # HEADER
    ###################
    def _gen_header(self, header_dict):
        text = ""
        text += "\\cvheader{%s}{%s}{%s}\n" % (self._gen_firstname(header_dict), self._gen_lastname(header_dict), self._gen_cvtitle(header_dict))
        text += "{%s}\n" % (self._gen_contactinfo(header_dict))
        return text
    def _gen_email(self, header_dict):
        return "\\href{mailto:%s}{\\faEnvelope~%s}" % (header_dict['e-mail'], header_dict['e-mail'])
    def _gen_phonenbr(self, header_dict):
        return "\\faPhone~%s" % (header_dict["phone_number"].replace(" ", "~"))
    def _gen_github(self, header_dict):
        return "\\href{https://github.com/%s}{\\faGithub~%s}" % (header_dict['github'], header_dict['github'])
    def _gen_orcid(self, header_dict):
        return "\\href{https://orcid.org/%s}{\\orcidlink{%s}~%s}" % (header_dict['orcid'],header_dict['orcid'],header_dict['orcid'])
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
        text = ""
        text += "\\needspace{2 \\baselineskip} \n"
        text += "\\section*{%s}" % (section_dict['title']) 
        return text
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
        return text
    def _gen_cvitem_title(self, item_dict):
        title = item_dict.get('title', '')
        date  = item_dict.get('date', '')
        formatted_title = "%s \\hfill %s" % (title, date)
        return "\\subsection*{%s}" % formatted_title
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
            text += "\\begin{itemize}\n"
            for item in item_dict['list']:
                text += "  \\item{%s}\n" % (item)
            text += "\\end{itemize}\n"
            return text
        return ""
    def _gen_table(self, item_dict):
        if "table" not in item_dict:
            return ""
        table = item_dict["table"]
        text = ""
        keys = table[0]
        values = table[1:]
        # Guess column type
        threshold = 30
        column_length = [0 for _ in keys]
        if False:
            for row in values:
                for i,cell in enumerate(row):
                    column_length[i] += len(cell)
            column_length = [x/len(values) for x in column_length]
        if True:
            for row in values:
                for i,cell in enumerate(row):
                    column_length[i] = max(column_length[i], len(cell))
        column_types = ["l" if x < threshold else "X" for x in column_length]
        # Build table
        text += "\\begin{table}[H] \n"
        text += "\\small \n"
        text += "\\begin{tabularx}{\\linewidth}{%s}\n" % ("".join(column_types))
        text += "% " + "Column widths (chars) : {%s}\n" % (", ".join([str(x) for x in column_length]))
        text += "\\toprule \n"
        head_text = f"{TABLE_AMPERSAND_PLACEHOLDER.join(["\\textbf{%s}" % x for x in keys])}".replace("\n", " \\newline ")
        text += f"{head_text} \\\\ \\midrule \n"
        for i,row in enumerate(values):
            row_text = f"{TABLE_AMPERSAND_PLACEHOLDER.join([str(x) for x in row])}".replace("\n", " \\newline ")
            text += f"{row_text} \\\\ "
            if i == len(values) - 1:
                text +=  "\\bottomrule \n"
            else:
                text +=  "\\midrule \n"
        text += "\\end{tabularx}\n"
        text += "\\end{table}\n"
        return text
    

CV = CVmakerLatex(
    input_file = "./cv_contents.json",
    output_file = "CV.tex"
)
CV.make()