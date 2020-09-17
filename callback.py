class CallbackDataFactory:
    str = ''
    data = {}
    last_item = dict()

    def __init__(self, inp):
        if type(inp) == str:
            self.str = inp
            self.parse_data()
        else:
            self.data = inp
            self.collect_data()
        self.get_last_item()

    def collect_data(self):
        self.str = ','.join([f'{key};{value}' for key, value in self.data.items()])

    def parse_data(self):
        elements = [element.split(';') for element in self.str.split(',')]
        self.data = {key: val for (key, val) in elements}

    def get_last_item(self):
        self.last_item['key'], self.last_item['value'] = self.str.split(',')[-1].split(';')

    def get_type(self):
        return f"type;{self.data['type']},"
