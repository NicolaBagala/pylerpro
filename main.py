from entry import Entry
from vault import Vault

print("PylerPro text interface. Type a command.")

current_vault = None 

while True: 
    prompt = f"[{current_vault.name}] > " if current_vault is not None else "[No vault loaded] > "
    command_parts = input(prompt).split()    
    
    if command_parts == [] or (command_parts[0] in ["new","edit", "show", "remove", "save", "load"] and len(command_parts) == 1):
        print("Invalid command or missing parameter. Try again.")
        continue
    elif command_parts[0] in ["save", "load"] and len(command_parts) < 3:
        print("To save or load a vault, you must provide its path a password. Try again.")
        continue
        
    match command_parts[0]: 
        case "new":
            if current_vault is not None:
                confirm_new = input("Any unsaved data will be lost. Confirm? (y/n) ")
                if confirm_new != "y":
                    continue
            current_vault = Vault(command_parts[1])            
        case "add":
            
            if current_vault is not None:
                title = input("Entry title: ")
                user = input("Username: ")
                pwd = input("Password: ")
                try: 
                    current_vault.add_entry(Entry(title, user, pwd))
                    print(f"Entry '{title}' added.")
                except Exception as e:
                    print(e)
            else:
                print("No vault selected, load or create one.")
        case "edit":

            if current_vault is not None:
                try:
                    current_vault.edit_entry(command_parts[1])
                    print(f"Entry '{command_parts[1]}' successfully edited.")
                except Exception as e:
                    print(e)
            else: 
                print("No vault selected, load or create one.")

        case "show":
            if current_vault is not None:
                if command_parts[1] == "all":
                    for entry in current_vault.get_entries():
                        print(entry)
                    print("")
                else:
                    try:
                        print(current_vault.get_entry(command_parts[1]))
                        print("")
                    except Exception as e:
                        print(e)
            else:
                print("No vault selected, load or create one.")

        case "remove":
            if current_vault is not None:
                confirm_rem = input(f"Remove entry '{command_parts[1]}'. Are you sure? (y/n) " )
                if confirm_rem.lower() == "y":
                    try:
                        current_vault.remove_entry(command_parts[1])
                        print("Entry successfully removed.")
                    except Exception as e:
                        print(e)                 
            else:
                print("No vault selected, load or create one.")

        case "save":
            if current_vault is not None:
                try:
                    current_vault.save(command_parts[1], command_parts[2])
                    print("Vault saved successfully.")
                except Exception as e:
                    print(e)

        case "load":
            if current_vault is None:                
                try:
                    current_vault = Vault.load(command_parts[1], command_parts[2])
                except Exception as e:
                    print(e)
            else:
                print("Save and close the current vault first.")

        case "close":
            if current_vault is not None:
                confirm_close = input("Any unsaved data will be lost. Confirm? y/n")
                if confirm_close != "y":
                    continue
            current_vault = None 

        case "exit":
            if current_vault is not None:
                confirm_close = input("Any unsaved data will be lost. Confirm? y/n")
                if confirm_close != "y":
                    continue            
            break
        case _:
            print("Unknown command")
    


            
                    
        



