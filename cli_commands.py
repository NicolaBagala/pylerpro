import utils, messages as msg
from getpass import getpass
from vault import Vault, Entry 



def dispatch(cmd, current_vault, params, flags):
    """
        Call cmd(current_vault, params, flags) to execute the desired command, 
        unless flags contain the -h option.
        If flags contains -h, display the help message for cmd and return None.

        Otherwise, return whatever the corresponding function call returns.
    """

    if "-h" in flags:
        utils.info(msg.CLI_HELP_MSG[cmd])
    else:
        return COMMANDS[cmd](current_vault, params, flags)


def new_command(current_vault, params, flags):
    """
        Create a new vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Retun a Vault object. May return None if vault creation is aborted.
    """

    vault_name = params[0]
    quiet = "-q" in flags 
    help = "-h" in flags     
    
    if not quiet and current_vault is not None:
        match utils.confirm(msg.OPEN_VAULT_ABORT_SAVE_CONTINUE):
            case "s":
                save_command(current_vault)                
            case "c":
                pass
            case _:
                return 
    password = getpass(f"Insert password for vault '{vault_name}': ")           
    return Vault.create(vault_name, password)

def show_command(current_vault, params, flags):
    """
        Show a specific entry or all entries in a vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.
    """

    entry_title = params[0] if len(params) > 0 else None 
    show_all = "-a" in flags

    if entry_title is None and not show_all:
        utils.info(msg.INSUFFICIENT_PARAMS_OR_FLAGS)
    elif current_vault is None: 
        utils.info(msg.NO_OPEN_VAULT)
    else:
        entries = current_vault.get_entries() if show_all else [current_vault.get_entry(entry_title)]
        if len(entries) == 0:
            utils.info(msg.EMPTY_VAULT.format(current_vault))
        else:
            for e in entries:
                print(e, "\n")        

def add_command(current_vault, params, flags):
    """
        Add a new entry to a vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: params and flags are mute variables, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """

    if current_vault is None:
        utils.info(msg.NO_OPEN_VAULT)
    else:
        title = input("Entry title: ")
        user = input("Username: ")
        pwd = getpass("Password: ")
                    
        current_vault.add_entry(Entry(title, user, pwd))

def edit_command(current_vault, params, flags):
    """
        Edit an existing entry in a vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: flags is a mute variable, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """

    entry_title = params[0]
    entry_field = params[1]
    new_value = params[2]

    if current_vault is None:
        utils.info(msg.NO_OPEN_VAULT)
    else:
        current_vault.edit_entry(entry_title, entry_field, new_value)

def remove_command(current_vault, params, flags):
    """
        Removes an entry from a vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: flags is a mute variable, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """

    entry_title = params[0]

    if current_vault is None:
        utils.inf(msg.NO_OPEN_VAULT)
    else:
        current_vault.remove_entry(entry_title)            

def save_command(current_vault, params, flags):
    """
        Save an open vault to disk.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: params and flags are mute variables, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """

    if current_vault is None:
        utils.info(msg.NO_OPEN_VAULT)
    else: 
        file_path = input("Path to save vault to: ")             
        current_vault.save(file_path)

def load_command(current_vault, params, flags):
    """
        Load a vault from disk.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Retun a Vault object. Can return none if vault loading was aborted.        
    """

    file_path = params[0]
    quiet = "-q" in flags    
    
    if not quiet and current_vault is not None:
        match utils.confirm(msg.OPEN_VAULT_ABORT_SAVE_CONTINUE):
            case "s":
                save_command(current_vault)                
            case "c":
                pass
            case _:
                return  
    
    password = getpass(f"Input password for {file_path}: ")
    return Vault.load(file_path, password)
    

def close_command(current_vault, params, flags):
    """
        Closes a currently open vault.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: params is a mute variable, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.

        Returns None, or the current vault if it isn't None and the user
        doesn't want to close it.
    """

    quiet = "-q" in flags 

    if current_vault is None:
        utils.info(msg.NO_OPEN_VAULT) 
        return None        
    else:
        if quiet or utils.confirm(msg.CONTINUE_WITHOUT_SAVING) == "Y":
            return None

    # If we got here, it means current_vault != None and we don't want to close it
    return current_vault

def exit_command(current_vault, params, flags):  
    """
        Exits the program.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: params is a mute variable, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """  

    quiet = "-q" in flags

    if quiet or utils.no_open_vault_or_continue_without_saving(current_vault):
        raise SystemExit

def cmds_list_command(current_vault, params, flags):
    """
        Displays a list of available commands.
        current_vault is a Vault object. Can be None.
        params and flags are lists, which can be empty.

        Note: current_vault, params and flags are mute variables, only needed in the signature
        to keep the dispatch function as command-agnostic as possible.
    """
    utils.info(msg.COMMAND_LIST)

COMMANDS = {
    "new": new_command,
    "add": add_command,
    "edit": edit_command,
    "show": show_command,
    "remove": remove_command,
    "save": save_command,
    "load": load_command,
    "close": close_command,
    "exit": exit_command,
    "commands": cmds_list_command
}

# If the value is a tuple, the first element is 
# the minimum number of expected parameters and
# the second one is the maximum.
EXP_PARAMS_PER_CMD = {
    "new": 1,
    "add": 0,
    "edit": 3,
    "show": (0,1),
    "remove": 1,
    "save": 0,
    "load": 1,
    "close": 0,
    "exit": 0,
    "commands": 0
}

VALID_CMD_FLAGS = {

    # -a: show all entries
    # -h: display help
    # -q: don't ask for confirmation

    "new": ("-h", "-q"),      
    "add": ("-h"),
    "edit": ("-h"),
    "show": ("-a", "-h"),
    "remove": ("-h"),
    "save": ("-h"),
    "load": ("-h", "-q"),
    "close": ("-h", "-q"),
    "exit": ("-h", "-q"),
    "commands": ("-h")
}