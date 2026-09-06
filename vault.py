from entry import Entry
import messages as msg, exceptions as ex, utils
import json, os, encryption
from cryptography.exceptions import InvalidTag

class Vault:
    def __init__(self, name, key, salt):
        """
            Initialize a Vault object.
            name is a string.
        """

        self.name = name
        self.entries = {}

        self._key = key
        self._salt = salt

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
            raise TypeError(msg.NOT_AN_ENTRY)

        if entry.title in self.entries: 
            raise ValueError(msg.ENTRY_ALREADY_EXISTS.format(entry.title, self.name))
        self.entries[entry.title] = entry
        
    def edit_entry(self, entry_title, entry_field, new_value):
        """
            Edit a specific property of an Entry.
            entry_title, entry_field, and new_value are strings.

            Raise:
                ValueError: if entry_field is not an editable entry field.
        """        
        
        if entry_field not in Entry.EDITABLE_FIELDS:
            raise ValueError(msg.INVALID_ENTRY_FIELD.format(entry_field))

        entry = self.get_entry(entry_title)

        # temporary shenanigan until UUID-indexing is implemented
        if entry_field == "title":

            if new_value in self.entries and new_value != entry.title:
                raise ValueError(msg.ENTRY_ALREADY_EXISTS.format(new_value, self.name))
            else:
                del self.entries[entry.title]
                entry.title = new_value
                self.entries[new_value] = entry 
        else:
            setattr(entry, entry_field, new_value)    

    def get_entry(self, entry_title):
        """
        Get an Entry from the vault.
        entry_title is a string.

        Raise:           
            ValueError: if the key entry_title can't be found in self.entries.
        """
        if entry_title not in self.entries:
            raise ValueError(msg.ENTRY_NOT_FOUND.format("retrieve", entry_title, self.name))
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
            raise ValueError(msg.ENTRY_NOT_FOUND.format("remove", entry_title, self.name))
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
    def from_dict(cls, data, key, salt):
        """
        Create and populate a vault from a dictionary.
        data is a dictionary representation of a vault.
        Return a vault object.
        """
        vault = cls(data["name"], key, salt)        
        for v in data["entries"].values():
            entry = Entry.from_dict(v)
            vault.add_entry(entry)
        return vault             
    
    def save(self, file_path):        
        """
        Save the vault as an encrypted JSON file in the given path.
        file_path is a string.
        """        
        
        vault_exists =  os.path.isfile(file_path)
        if vault_exists: ans = utils.confirm(msg.VAULT_ALREADY_EXISTS.format(file_path))
        proceed = not vault_exists or ans == "y"            

        if proceed:
            encrypted_data, nonce = encryption.encrypt(self._key, json.dumps(self.to_dict(), indent = 1))        
            sev_s = encryption.serialize_encrypted_vault(self._salt, nonce, encrypted_data)
            
            with open(f"{file_path}", "wb") as f:
                f.write(sev_s)
            utils.info(msg.VAULT_SAVED)            

        
    
    @classmethod
    def load(cls, file_path, password):
        """
        Load a vault from an encrypted JSON file stored in file_path.
        password and file_path are strings.
        Return a decrypted vault.

        """
        try:
            with open(f"{file_path}", "rb") as f:
                vault_file = f.read()
                # The magic is not needed for now, but won't hurt to leave it...
                magic, salt, nonce, encrypted_data = encryption.deserialize_encrypted_vault(vault_file)                

                key = encryption.derive_key(password, salt)                
                decrypted_data = encryption.decrypt(key, nonce, encrypted_data)                            
                return cls.from_dict(json.loads(decrypted_data), key, salt)
        except InvalidTag:
            raise ex.FailedToLoadVault(msg.FAILED_TO_LOAD_VAULT.format(file_path))
        

    @classmethod
    def create(cls, vault_name, password):
        """
            Create a new vault.
            Derive an encryption key from password and generate a salt.
            vault_name and password are strings.
        """
        
        salt = os.urandom(encryption.SALT_SIZE)
        key = encryption.derive_key(password, salt)

        return cls(vault_name, key, salt)

    # Validation methods
    @staticmethod
    def vault_file_exists(file_path):
        return os.path.isfile(file_path)


