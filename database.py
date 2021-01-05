from contact import Contact


# TODO update and delete methods
class Database:
    def __init__(self):
        self.__contacts = []
        self.__latest_contact_id = 0
        self.add_contact(Contact('Daniel', '123', 'note1'))
        self.add_contact(Contact('Devin', '456', 'note2'))

    def get_contacts(self):
        return self.__contacts

    def get_contact_by_id(self, id_):
        for contact in self.__contacts:
            if contact.id == id_:
                return contact
        print('No contact with such id')
        return None

    # TODO check if contact has no id
    def add_contact(self, contact):
        if contact.id != -1:
            return False
        contact.id = self.__latest_contact_id
        self.__latest_contact_id += 1
        self.__contacts.append(contact)
        return True

    def update_contact(self, contact_id, new_name, new_number, new_note):
        contact = self.get_contact_by_id(contact_id)
        # TODO check if the contact exists
        contact.name = new_name
        contact.number = new_number
        contact.note = new_note

    def delete_contact(self, contact_id):
        self.__contacts.remove(self.get_contact_by_id(contact_id))
