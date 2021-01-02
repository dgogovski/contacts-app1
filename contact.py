class Contact:
    def __init__(self, name, number, note):
        self.id = -1
        self.name = name
        self.number = number
        self.note = note

    def get_data(self):
        contact_data = [self.name, self.number, self.note]
        return contact_data

    def set_name(self, name):
        self.name = name
