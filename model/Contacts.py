from model.pim_model import Item


class Contact(Item):
    def __init__(self, name, phone, email, address, load):
        super().__init__("Contacts", load)
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\n"

    def create_item(self, item_data):
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
