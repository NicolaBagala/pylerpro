from entry import Entry
from vault import Vault

# entry = Entry(
#     title = "Test entry",
#     username = "user",
#     password = "pwd"
# )

# entry2 = Entry(
#     title = "Test entry2",
#     username = "user2",
#     password = "pwd2"
# )

# vault = Vault("Test vault")

try:
    vault = Vault.load("Test vault.json")
    print(vault)
    for k in vault.entries.values():
        print(k)

except Exception as e:
    print(e)



