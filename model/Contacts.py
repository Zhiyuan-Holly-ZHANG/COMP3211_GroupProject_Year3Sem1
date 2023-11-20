from model.Item import Item


class Contact(Item):
    def __init__(self, name, phone, email, address, load):
        super().__init__("Contacts", load)
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def create_item(self, item_data):
        print("called")
        return Contact(item_data['Name'], item_data['Phone'], item_data['Email'], item_data['Address'], self.load)

    def add_contact(self, name, phone, email, address):
        event_data = {
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Address": address
        }
        self.save_to_file(event_data)
        self.update()
