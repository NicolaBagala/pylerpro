from entry import Entry
import json 

class Vault:
    def __init__(self, name):
        self.name = name
        self.entries = {}

    def __str__(self):        
        return (
            f"Vault name: {self.name}\n"
            f"Entries stored: {len(self.entries)}"
        )

    
    def add_entry(self, entry):
        """
        Add an Entry to the vault.

        Raises:
            TypeError: if entry is not an Entry.
            ValueError: if another entry has the same title.
        """
        if not isinstance(entry, Entry): 
            raise TypeError("An object of type other than Entry was passed to add_entry. This method only accepts objects of the Entry type.")

        if entry.title in self.entries: 
            raise ValueError(f"An entry with title '{entry.title}' already exists in vault '{self.name}'.")
        self.entries[entry.title] = entry
        
    def edit_entry(self, entry_title):
        """
            Edit an entry by directly modifying its properties. 
            This method is temporary, for command line testing, and likely to change later on.
        """        
        entry = self.get_entry(entry_title)
        print("Specify the new values of the entry. Blank + enter to leave unchanged.")
        new_title = input("New title: ")
        new_username = input("New username: ")
        new_password = input("New password: ")

        entry.title = new_title if new_title != "" else entry.title
        entry.username = new_username if new_username != "" else entry.username
        entry.password = new_password if new_password != "" else entry.password
        
        self.remove_entry(entry_title)
        self.add_entry(entry)

    def get_entry(self, entry_title):
        """
        Get an Entry from the vault.

        Raises:           
            ValueError: if the entry can't be found in the vault.
        """
        if entry_title not in self.entries:
            raise ValueError(f"Cannot retrieve entry '{entry_title}': entry not found in vault '{self.name}'.")
        return self.entries[entry_title]
    
    def get_entries(self):
        """
        Return a collection of all entries.
        """
        return self.entries.values()
    
    def remove_entry(self, entry_title):
        """
        Remove an Entry from the vault.

        Raises:           
            ValueError: if the entry can't be found in the vault.
        """
        if entry_title not in self.entries:
            raise ValueError(f"Cannot remove entry '{entry_title}': entry not found in vault '{self.name}'.")
        del self.entries[entry_title]

    def to_dict(self):
        """
        Return a dictionary representation of the vault.
        """
        return {
                "name": self.name,
                "entries": {k: v.to_dict() for k, v in self.entries.items()}
                }   

    @classmethod
    def from_dict(cls, data):
        """
        Create and populate a vault from a dictionary.
        """
        vault = cls(data["name"])        
        for v in data["entries"].values():
            entry = Entry.from_dict(v)
            vault.add_entry(entry)
        return vault             
    
    def save(self, file_path):        
        """
        Save the vault in JSON format in the project's root.
        """
        with open(f"{file_path}", "w") as f:            
            json.dump(self.to_dict(), f, indent = 1)       
    
    @classmethod
    def load(cls, file_path):
        """
        Load a vault from a JSON file.
        """
        with open(f"{file_path}") as f:
            return cls.from_dict(json.load(f))


