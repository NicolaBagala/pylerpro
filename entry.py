class Entry:
    def __init__(self, title, username, password):
        self.title = title
        self.username = username
        self.password = password 

    def __str__(self):
        return """
        Entry title: {}
        Entry username: {}
        Entry password: {}
        """.format(self.title, self.username, self.password)

        
    
