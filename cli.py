from entry import Entry
from vault import Vault
import cli_commands as clic, utils, messages as msg, exceptions as ex

current_vault = None
print("PylerPro text interface. Type a command. Type 'commands' for a list of available commands.")

def parse_command(cmd_str):
    """
        Separate cmd_str into a command and any additional parameters and flags.
        Verify that the given command/parameters/flags are valid.
        
        Raise:
            InvalidCommand: the command provided doesn't exist.
            InvalidNumberOfParameters: the parameters provided are less or more than expected.
            InvalidCommandFlag: the flags provided are not valid.

        Return a tuple of the form (cmd, params, flags), where cmd is a string and
        params and flags are lists, which can be empty.
    """
    cmd_parts = cmd_str.split()
    cmd = cmd_parts[0] if len(cmd_parts) > 0 else ""
    args = cmd_parts[1:] if len(cmd_parts) > 1 else []   

    flags = [a for a in args if a[0] == "-"]
    params = [a for a in args if a not in flags]

    # If the -h flag is provided, the dispatcher is called regardless.
    help = "-h" in flags
    
    if cmd not in clic.COMMANDS:        
        raise ex.InvalidCommand(msg.INVALID_COMMAND.format(cmd))        

    given_params = len(params)    
    exp_params = clic.EXP_PARAMS_PER_CMD[cmd]

    min_exp_params = exp_params[0] if type(exp_params) == tuple else exp_params
    max_exp_params = exp_params[1] if type(exp_params) == tuple else exp_params
        
    if not help and ((given_params < min_exp_params) or (given_params > max_exp_params)): 
        params_msg = utils.format_invalid_num_params_msg(exp_params)
        raise ex.InvalidNumberOfParameters(msg.INVALID_NUMBER_OF_PARAMS.format(cmd, params_msg, given_params))

    if not help:
        for f in flags: 
            if f not in clic.VALID_CMD_FLAGS[cmd]:
                raise ex.InvalidCommandFlag(msg.INVALID_FLAG.format(f, cmd))
        
    return cmd, params, flags


while True:
    prompt = f"[{current_vault.name}] > " if current_vault is not None else "[No vault loaded] > "
    cmd_str = input(prompt)

    try:
        cmd, params, flags = parse_command(cmd_str)
        cmd_return_value = clic.dispatch(cmd, current_vault, params, flags)

        #if isinstance(cmd_return_value, Vault) or cmd == "close": 
        current_vault = cmd_return_value

    except Exception as e:        
        utils.info(str(e))
          
    