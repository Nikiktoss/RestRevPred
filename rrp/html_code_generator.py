class HTMlCodeGenerator:
    cities = {'İstanbul': 'Istanbul', 'Diyarbakır': 'Diyarbakir', 'İzmir': 'Izmir', 'Elazığ': 'Elazıg',
              'Eskişehir': 'Eskisehir', 'Şanlıurfa': 'Sanliurfa', 'Uşak': 'Usak', 'Muğla': 'Mugla',
              'Kırklareli': 'Kirklareli', 'Karabük': 'Karabuk', 'Tekirdağ': 'Tekirdag', 'Balıkesir': 'Balikesir',
              'Aydın': 'Aydin', 'Kütahya': 'Kutahya'}

    @staticmethod
    def write_table_header(columns):
        header = ""

        for column in columns:
            header += f'<th style="border-right: 2px solid black; text-align: center;">{column}</th>\n'

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
                row += f'<td style="border-right: 2px solid black; text-align: center;">{value}</td>\n'
            elif type(value) != str:
                row += f'<td style="border-right: 2px solid black; text-align: center;">' \
                       f'{float(value):.{num_of_symbols}f}</td>\n'
            else:
                row += f'<td style="border-right: 2px solid black; text-align: center;">{value}</td>\n'

        return row

    def create_table(self, columns, values):
        table = ""
        num_of_tables = (len(columns) // 10) + 1

        for i in range(num_of_tables):
            if i == num_of_tables - 1:
                header = self.write_table_header(columns[i * 10:])
                row = self.write_table_row(values[i * 10:])
            else:
                header = self.write_table_header(columns[i * 10: (i + 1) * 10])
                row = self.write_table_row(values[i * 10: (i + 1) * 10])

            table += f'''<table style="width: 100%; margin-bottom: 15px;">
                            <tr style="border-bottom: 2px solid black;">
                                {header}
                            </tr>
                            <tr>{row}</tr>
                         </table>\n'''

        return table

    def table_element(self, title, columns, values):
        result = f'''<div class="table_element">
                        <p class="table_title">{title}:</p>\n'''

        result += self.create_table(columns, values)
        result += '</div>'

        return result

    def generate_html(self, num_data, cat_data, normalize_num_data, normalize_cat_data, revenue):
        result = '''
                 <div class="show_result">
                    <p class="input_data_title">Input data</p>'''

        result += self.table_element('Category data', cat_data.columns, cat_data.values[0])
        result += self.table_element('Numeric data', num_data.columns, num_data.values[0])

        result += '<p class="input_data_title">Normalize data</p>\n'
        result += self.table_element('Category data', normalize_cat_data.columns, normalize_cat_data.values[0])
        result += self.table_element('Numeric data', normalize_num_data.columns, normalize_num_data.values[0])

        result += f'<p class="prediction_title">Final result:</p><p><b>{ revenue }</b></p></div>'

        return result
