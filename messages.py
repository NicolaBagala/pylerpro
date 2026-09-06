# Generic messages
CONTINUE_WITHOUT_SAVING = "Any unsaved data will be lost. Continue? (y/n; default: no)"
INVALID_COMMAND = "'{}' is not a valid command. Try again."
INVALID_NUMBER_OF_PARAMS = "'{}' expects {}, but {} were given."
INVALID_FLAG = "'{}' is not a valid flag for command '{}'."
INSUFFICIENT_PARAMS_OR_FLAGS = 'This command needs at least one parameter or a flag.'
FIELD_CANNOT_BE_EMPTY = "This field cannot be empty."

# Vault messages
NO_OPEN_VAULT = "No vault is currently open."
EMPTY_VAULT = "The selected vault is empty."
FAILED_TO_LOAD_VAULT = "'{}' is not a valid vault, or the password provided was incorrect."
OPEN_VAULT_ABORT_SAVE_CONTINUE = "A vault is currently open. Save and close (s), continue without saving (c), or abort (a; default)?"
VAULT_ALREADY_EXISTS = "A vault already exists in location '{}'. Continue? (y/n; default: no)"
VAULT_SAVED = "Vault saved successfully."
PASSWORD_FOR_NEW_VAULT = "Insert password for vault '{}': "
PASSWORD_TO_LOAD_VAULT = "Inser password to load '{}': "
VAULT_PATH = "Path to save vault to: "
INVALID_PATH = "'{}' is not a valid path."


# Entry messages
NOT_AN_ENTRY = "An object of type other than Entry was passed to add_entry. This method only accepts objects of the Entry type."
ENTRY_ALREADY_EXISTS = "An entry with title '{}' already exists in vault '{}'."
ENTRY_NOT_FOUND = "Cannot '{}' entry '{}': entry not found in vault '{}'."
INVALID_ENTRY_FIELD = "'{}' is not a valid entry field."



# CLI help
COMMAND_LIST = """
Available commands

    new: Create a new vault
    show: Display vault entries
    add: Add an entry to a vault
    edit: Edit an entry in a vault
    remove: Remove an entry from a vault
    save: Save a vault to disk
    load: Load a vault from disk
    close: Close an open vault
    exit: Exit the program
    commands: Display this list

All commands are case-sensitive. Type <command> -h for command-specfic help.

Default answers to confirmations can be given with any string. Example:

""Any unsaved data will be lost. Continue? (y/n; default: no)"
y or Y: yes
n, N, any string except y or Y, or just [enter]: no
"""

CLI_HELP_MSG = {
    "new": """Usage: new <vault_name> [-q][-h]
    Creates a new vault called vault_name. If the -q flag is provided, it will
    proceed without asking for confirmation even if another vault is currently open.
    If -q is not provided and another vault is open, it will ask whether 
    to save before proceeding, continue without saving, or abort.

    -h displays this message, other options are ignored.
    
    Asks for a password upon creating a new vault.""",

    "show": """Usage: show [entry_title] [-a][-h]
    Shows the entry called entry_title if provided, or all entries in the currently open vault
    if the -a flag is give. Either entry_title or -a must be provided. If both are provided, 
    entry_title will be ignored and all entries will be displayed.
    Raises an error if entry_title can't be found.

    -h displays this message, other options are ignored.    
    """,

    "add": """Usage: add [-h]
    Adds a new entry to an existing open vault. Prompts the user for the new entry's
    title, username, and password.

    -h displays this message.    
    """,

    "edit": """Usage: edit <entry_title> <entry_field> <new_value> [-h]
    Edits an existing entry in a currently open vault using the provided parameters. 
    All three parameters are compulsory. Raises an error if entry_title can't be found.

    -h displays this message, other options are ignored.
    """,

    "remove": """Usage remove <entry_title> [-h]
    Removes an existing entry from a currently open vault. 
    Raises an error if entry_title can't be found.

    -h displays this message, other options are ignored.
    """,

    "save": """Usage save <file_path> [-h]
    Savs a currently open vault to disk in the specified file_path. 
    If file_path already exists, it will be overwritten.

    -h displays this message, other options are ignored.
    """,

    "load": """Usage: load <file_path> [-q][-h]
    Loads from disk a vault stored in file_path. If the -q flag is provided, 
    it will proceed without asking confirmation even if another vault is currently
    open, potentially causing the loss of unsaved data. Otherwise, it will ask
    whether to save before proceeding, continuing without saving, or aborting.

    -h displays this message, other options are ignored.
    """,

    "close": """Usage: close [-q][-h]
    Closes the currently open vault. If the -q flag is provided, it will proceed
    without asking for confimation.
    
    -h displays this message, other options are ignored.
    """,

    "exit": """Usage: exit [-q][-h]
    Exits the program. If the -q flag is provided, it will proceed without asking
    for confirmation, even if a vault is currently open, potentially causing the loss
    of unsaved data.

    -h displays this message, other options are ignored.
    """,

    "commands": """Usage: commands [-h]
    Displays a list of available commands.

    -h displays this message, other options are ignored.
    """




}

