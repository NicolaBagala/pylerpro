class Entry:
    def __init__(self, title, username, password):
        """
            Intialize an Entry object.
            title, username, and password are strings.
        """
        self.title = title
        self.username = username
        self.password = password 

    def __str__(self):
        """
            Return a pretty-printed representation of an Entry object.
        """
        return (
        f"Entry title: {self.title}\n"
        f"Entry username: {self.username}\n"
        f"Entry password: {self.password}"
        )
    
    @classmethod
    def from_dict(cls, data):
        """
        Instantiate and populate an Entry object from a dictionary.
        data is a dictionary representation of an Entry.
        Return an Entry object.
        """
        return cls(
            title = data["title"],
            username = data["username"],
            password = data["password"]
        )
        
    def to_dict(self):
        """
        Return a dictionary representation of an Entry.
        """
        return {"title": self.title, 
                "username": self.username,
                "password": self.password
                }
