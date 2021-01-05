class Contact:
    def __init__(self, name, number, note):
        self.id = -1
        self.name = name
        self.number = number
        self.note = note

    def set_name(self, name):
        self.name = name
