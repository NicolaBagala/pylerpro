import messages as msg

def format_invalid_num_params_msg(exp_params):
    """
        Format and return a substring of the INVALID_NUMBER_OF_PARAMS message.
        exp_params can be an int representing the exact number of expected parameters
        or a tuple of the form (m, M), representing the minimum and maximum number of
        parameters expected.

        Return a string.
    """

    if type(exp_params) == int:
        return "{} parameter{}".format(exp_params, "s" if exp_params > 1 else "")
    # If the above doesn't happen, exp_params is a tuple    
    return f"between {exp_params[0]} and {exp_params[1]} parameters"
        

def confirm(qstn):
    """
        Prompt the user with qstn, and return the user's answer.
        qstn is a string.
        Return a string.
    """
    return input(qstn)

def info(msg, *args):
    """
        Display an info message.
        Populate msg with args if any, and print the resulting string.
        msg and *args are strings.
    """
    print(msg.format(*args))

def no_open_vault_or_continue_without_saving(current_vault):
    """
        Determine whether at least either condition is true: there is no currently
        open vault or the user wants to continue without saving.
        current_vault is a Vault object. Can be None. 
        Return a boolean.
    """
    no_open_vault = current_vault is None     
    continue_without_saving = False if no_open_vault else confirm(msg.CONTINUE_WITHOUT_SAVING) == "Y"
    
    return no_open_vault or continue_without_saving    


