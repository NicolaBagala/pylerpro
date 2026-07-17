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
        
    def to_dict(self):
        return {"title": self.title, 
                "username": self.username,
                "password": self.password
                }
