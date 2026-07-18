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
        if not type(entry) is Entry: 
            raise TypeError("An object of type other than Entry was passed to add_entry. This method only accepts objects of the Entry type.")

        if entry.title in self.entries: 
            raise ValueError(f"An entry with title '{entry.title}' already exists in vault '{self.name}'.")
        self.entries[entry.title] = entry
        
    def get_entry(self, entry_title):
        if entry_title not in self.entries:
            raise ValueError(f"Cannot retrieve entry '{entry_title}': entry not found in vault '{self.name}'.")
        return self.entries[entry_title]
    
    def remove_entry(self, entry_title):
        if entry_title not in self.entries:
            raise ValueError(f"Cannot remove entry '{entry_title}': entry not found in vault '{self.name}'.")
        del self.entries[entry_title]

    def to_dict(self):
        return {
                "name": self.name,
                "entries": {k: v.to_dict() for k, v in self.entries.items()}
                }   

    @classmethod
    def from_dict(cls, dict):
        vault = Vault(dict["name"])        
        for v in dict["entries"].values():
            entry = Entry.from_dict(v)
            vault.add_entry(entry)
        return vault             
    
    def save(self):        
        with open(f"{self.name}.json", "w") as f:            
            json.dump(self.to_dict(), f, indent = 1)       
    
    @classmethod
    def load(cls, file_name):
        with open(f"{file_name}") as f:
            return cls.from_dict(json.load(f))


