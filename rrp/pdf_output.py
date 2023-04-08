from fpdf import FPDF, HTMLMixin


class PDF(FPDF, HTMLMixin):
    cities = {'İstanbul': 'Istanbul', 'Diyarbakır': 'Diyarbakir', 'İzmir': 'Izmir', 'Elazığ': 'Elazıg',
              'Eskişehir': 'Eskisehir', 'Şanlıurfa': 'Sanliurfa', 'Uşak': 'Usak', 'Muğla': 'Mugla',
              'Kırklareli': 'Kirklareli', 'Karabük': 'Karabuk', 'Tekirdağ': 'Tekirdag', 'Balıkesir': 'Balikesir',
              'Aydın': 'Aydin', 'Kütahya': 'Kutahya', 'Niğde': 'Nigde'}

    def __init__(self, orientation='P', unit='mm', format='A4', rgb_color=(17, 14, 173)):
        super().__init__(orientation, unit, format)
        self.rgb_color = rgb_color

    def create_table(self, columns, values):
        num_of_tables = (len(columns) // 10) + 1

        for i in range(num_of_tables):
            if i == num_of_tables - 1:
                header = self.write_table_header(columns[i * 10:])
                row = self.write_table_row(values[i * 10:])
            else:
                header = self.write_table_header(columns[i * 10: (i + 1) * 10])
                row = self.write_table_row(values[i * 10: (i + 1) * 10])

            if self.will_page_break(20) is True:
                self.add_page()

            self.write_html(f"""<table width="100%" border="1">
                  <thead>
                    <tr>
                      {header}
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      {row}
                    </tr>
                  </tbody>
                </table>""")

    @staticmethod
    def write_table_header(columns):
        header = ""

        for column in columns:
            header += f"<th>{column}</th>\n"

        return header

    @classmethod
    def write_table_row(cls, values):
        row = ""
        num_of_symbols = 2

        if len(values) < 10:
            num_of_symbols = 5

        for value in values:
            if value in cls.cities:
                value = cls.cities[value]
                row += f"<td align='center'>{value}</td>\n"
            elif type(value) != str:
                row += f"<td align='center'>{float(value):.{num_of_symbols}f}</td>\n"
            else:
                row += f"<td align='center'>{value}</td>\n"

        return row

    def block_table(self, table_name, columns, values, table_size=16):
        self.set_text_color(self.rgb_color)
        self.set_font("Arial", size=16)

        self.cell(200, 5, txt=f"{table_name}", ln=1)

        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=table_size)
        self.create_table(columns, values)

    def block_result(self, result):
        self.set_font("Arial", size=18)
        self.set_text_color(self.rgb_color)

        self.cell(200, 15, txt="Final result:", ln=1)

        self.set_text_color(0, 0, 0)
        self.cell(200, 10, txt=f"{result}", ln=1)

    def block_title(self, title):
        self.set_font("Arial", size=16)
        self.set_text_color(self.rgb_color)

        self.cell(200, 20, txt=f"{title}", align="C", ln=1)


def generate_pdf_file(pdf_file, num_data, cat_data, normalize_num_data, normalize_cat_data, revenue):

    pdf_file.add_page()
    pdf_file.set_font("Arial", size=18)
    pdf_file.cell(200, 10, txt="Restaurant revenue prediction result", align="C", ln=1)

    pdf_file.block_title("Input data")
    pdf_file.block_table("Category data:", cat_data.columns, cat_data.values[0])
    pdf_file.block_table("Numeric data:", num_data.columns, num_data.values[0], 10)

    pdf_file.block_title("Normalize data")
    pdf_file.block_table("Category data:", normalize_cat_data.columns, normalize_cat_data.values[0])
    pdf_file.block_table("Numeric data:", normalize_num_data.columns, normalize_num_data.values[0], 10)

    pdf_file.block_result(revenue[0])
