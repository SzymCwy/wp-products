import pandas as pd

columns = ['ID', 'Typ', 'SKU', 'Nazwa', 'Opublikowano', 'Wyróżniony produkt?', 'Widoczność w katalogu', 'Krótki opis',
           'Opis', 'Data rozpoczęcia promocji', 'Data zakończenia promocji', 'Status podatku', 'Klasa podatkowa',
           'W magazynie?', 'Stan magazynowy', 'Niski stan magazynowy',
           'Pozwalać na zamówienia oczekujące (na dostawę do magazynu)?', 'Sprzedawany pojedynczo?', 'Waga (kg)',
           'Długość (cm)', 'Szerokość (cm)', 'Wysokość (cm)', 'Włącz opinie klientów?', 'Notatka do zakupu',
           'Cena promocyjna', 'Cena', 'Kategorie', 'Tagi', 'Klasa wysyłkowa', 'Obrazki', 'Limit pobrań',
           'Ważność pobierania', 'Element nadrzędny', 'Produkty grupowe', 'Produkty "up-sell"', 'Produkty "Cross-sell"',
           'Zewnętrzny adres URL', 'Tekst przycisku', 'Pozycja', 'Nazwa atrybutu 1', 'Wartości atrybutu 1',
           'Atrybut 1 widoczny', 'Atrybut 1: globalny', 'Pola: _wpcom_is_markdown',
           'Pola: neve_meta_enable_content_width', 'Pola: neve_meta_sidebar']

template = ['', '1', '0', 'visible', '', '', 'taxable', '1', '', '', '0', '0', '', '', '', '', '', '',
            '', '', '',
            'https://www.hossa-komfort-dom.eu/wp-content/uploads/2021/12/Swisspor-Plus-fasada''-0032-1.jpg',
            '', '', '', '', '', '', '', '', 'Grubość']

sheet = 'styropian.xlsx'


class CreateProduct:

    def __init__(self, product_columns, sheetdir):
        self.sheetdir = sheetdir
        self.product_columns = product_columns
        self.df = None
        self.variations = None
        self.price = None
        self.name = None
        self.piece = None
        self.m3 = None
        self.m2 = None
        self.description = None
        self.new_df = None

    def create_empty_df(self):
        self.new_df = pd.DataFrame(columns=self.product_columns)
        print(self.new_df)

    def read_csv(self):
        df = pd.read_excel(self.sheetdir, na_filter=False)
        self.name = df['Nazwa:'].tolist()
        self.price = df['Cena:'].tolist()
        self.description = df['Opis:'].tolist()
        self.variations = df['wariacje:'].tolist()
        self.m3 = df['m3'].tolist()
        self.m2 = df['m2'].tolist()
        self.piece = df['szt'].tolist()

    def ready_list(self):
        self.variations = [x for x in self.variations if x]  # if nan occurs
        for i in range(len(self.variations)):
            self.variations[i] = self.variations[i].split(',')
        self.piece = [x for x in self.piece if x]
        for i in range(len(self.piece)):
            self.piece[i] = self.piece[i].split(';')
        self.m3 = [x for x in self.m3 if x]
        for i in range(len(self.m3)):
            self.m3[i] = self.m3[i].split(';')
        self.m2 = [x for x in self.m2 if x]
        for i in range(len(self.m2)):
            self.m2[i] = self.m2[i].split(';')

    def fill_df(self):
        single_row = []
        single_row += template
        product_id = 1
        for i in range(len(self.name)):
            temp_pos = 0
            temp_var = 0
            single_row.insert(0, str(product_id))
            single_row.insert(1, 'variable')  # type
            single_row.insert(3, self.name[i])  # name
            single_row.insert(7, self.name[i])  # short desc
            single_row.insert(8, f'{self.description[i]},\\n cena za m³ - {self.price[i]}')  # desc
            single_row.insert(12, '')  # class
            single_row.insert(22, '1')
            single_row.insert(25, '')  # price
            single_row.insert(32, '')  # PARENT
            single_row.insert(40, ", ".join(self.variations[i]))  # att value
            single_row.insert(41, '1')  # att visible
            single_row.insert(42, '0')
            single_row.insert(43, '1')
            single_row.insert(44, 'off')
            single_row.insert(45, 'full-width')
            series = pd.Series(single_row, index=self.product_columns)
            self.new_df = self.new_df.append(series, ignore_index=True)
            single_row.clear()
            single_row += template
            parent_id = product_id
            product_id += 1
            temp_pos += 1
            for v in range(len(self.variations[i])):
                single_row.insert(0, str(product_id))  # id
                single_row.insert(1, 'variation')  # type
                single_row.insert(3, f'{self.name[i]} - {self.variations[i][v]}')  # name
                single_row.insert(7, '')
                single_row.insert(8, f'm³ = {self.m3[i][v]} \\n m²= {self.m2[i][v]} \\n sztuki w opakowaniu: '
                                          f'{self.piece[i][v]}')  # desc
                single_row.insert(12, 'parent')
                single_row.insert(22, '0')
                single_row.insert(25, round(float(self.price[i]) * float(self.m3[i][v]), 2))  # price
                single_row.insert(32, f'id:{int(parent_id)}')  # PARENT
                single_row.insert(40, self.variations[i][v])  # att value
                single_row.insert(41, '0')  # att visible
                single_row.insert(42, '0')
                single_row.insert(43, '')
                single_row.insert(44, '')
                single_row.insert(45, '')
                series = pd.Series(single_row, index=self.product_columns)
                self.new_df = self.new_df.append(series, ignore_index=True)
                single_row.clear()
                single_row += template
                temp_var += 1
                product_id += 1
                temp_pos += 1
        self.new_df.to_csv('siema.csv', index=False)


product = CreateProduct(columns, sheet)
product.create_empty_df()
product.read_csv()
product.ready_list()
product.fill_df()
