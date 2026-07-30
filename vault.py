from entry import Entry
import json, os, encryption

class Vault:
    def __init__(self, name):
        """
            Initialize a Vault object.
            name is a string.
        """

        self.name = name
        self.entries = {}

    def __str__(self):    
        """
            Return a pretty-printed string representation of a Vault object.
        """    
        return (
            f"Vault name: {self.name}\n"
            f"Entries stored: {len(self.entries)}"
        )

    
    def add_entry(self, entry):
        """
        Add an Entry to the vault.
        entry is an Entry object.

        Raise:
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
            entry_title is a string.
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
        entry_title is a string.

        Raise:           
            ValueError: if the key entry_title can't be found in self.entries.
        """
        if entry_title not in self.entries:
            raise ValueError(f"Cannot retrieve entry '{entry_title}': entry not found in vault '{self.name}'.")
        return self.entries[entry_title]
    
    def get_entries(self):
        """
        Return a collection of all entry objects stored in the vault.
        """
        return self.entries.values()
    
    def remove_entry(self, entry_title):
        """
        Remove an Entry with key entry_title from the vault.

        Raise:           
            ValueError: if the key entry_title can't be found in self.entries.
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
        data is a dictionary representation of a vault.
        Return a vault object.
        """
        vault = cls(data["name"])        
        for v in data["entries"].values():
            entry = Entry.from_dict(v)
            vault.add_entry(entry)
        return vault             
    
    def save(self, file_path, password):        
        """
        Save the vault as an encrypted JSON file in the given path.
        file_path and password are strings.
        """
        salt = os.urandom(16)
        key = encryption.derive_key(password, salt)

        encrypted_data, nonce = encryption.encrypt(key, json.dumps(self.to_dict(), indent = 1))
        key = None # The key is removed from memory immediately after use for safety reasons.

        sev_s = encryption.serialize_encrypted_vault(salt, nonce, encrypted_data)

        with open(f"{file_path}", "wb") as f:
            f.write(sev_s)
    
    @classmethod
    def load(cls, file_path, password):
        """
        Load a vault from an encrypted JSON file stored in file_path.
        password and file_path are strings.
        Return a decrypted vault, or None if the user aborts decryption.

        """
        with open(f"{file_path}", "rb") as f:
            vault_file = f.read()
            magic, salt, nonce, encrypted_data = encryption.deserialize_encrypted_vault(vault_file)

            attempt_decrypt = True
            if magic != encryption.FILE_MAGIC:
                attempt_decrypt = input("Selected file doesn't appear to be a Pylerpro vault. Attempt decryption anyway? (Y/n): ") == "Y"                

            if attempt_decrypt:
                key = encryption.derive_key(password, salt)                
                decrypted_data = encryption.decrypt(key, nonce, encrypted_data)                            
                return cls.from_dict(json.loads(decrypted_data))

            print("Decryption aborted.")
            return None 


