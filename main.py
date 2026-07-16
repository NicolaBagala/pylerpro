from entry import Entry
from vault import Vault

entry = Entry(
    title = "Test entry",
    username = "user",
    password = "pwd"
)

vault = Vault("Test vault")

try:
    vault.add_entry(entry)    
    print(vault.get_entry("Tesssst entry"))
except Exception as e:
    print(e)



