from entry import Entry

class Vault:
    def __init__(self, name):
        self.name = name
        self.entries = {}

    def add_entry(self, entry):
        if not type(entry) is Entry: 
            raise TypeError("An object of type other than Entry was passed to add_entry. This method only accepts objects of the Entry type.")

        if entry.title in self.entries: 
            raise ValueError("An entry with title '{}' already exists in vault '{}'.".format(entry.title, self.name))
        self.entries[entry.title] = entry

        
    def get_entry(self, entry_title):
        if entry_title not in self.entries:
            raise ValueError("An entry with title '{}' could not be found in vault '{}'.".format(entry_title, self.name))
        return self.entries[entry_title]
    

