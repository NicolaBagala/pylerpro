class Entry:
    def __init__(self, title, username, password):
        self.title = title
        self.username = username
        self.password = password 

    def __str__(self):
        return (
        f"Entry title: {self.title}\n"
        f"Entry username: {self.username}\n"
        f"Entry password: {self.password}"
        )
    
    @classmethod
    def from_dict(cls, data):
        """
        Instantiate and populate an entry from a dictionary.
        """
        return Entry(
            title = data["title"],
            username = data["username"],
            password = data["password"]
        )
        
    def to_dict(self):
        """
        Return a dictionary representation of the entry.
        """
        return {"title": self.title, 
                "username": self.username,
                "password": self.password
                }
