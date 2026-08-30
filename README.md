# pylerpro
A password manager written in Python as a software design and learning project.
NOTE: pylerpro is a work in progress and not intended for production use. I'm not a security expert and I don't recommend to use this software to store your passwords. I take no responsibility if you choose to do so.


v0.4 - CLI overhaul
- The main update in this version is a full CLI overhaul: instead of a giant match statement in the REPL, initially put there just to get started, the CLI is now divided into a parser, a dispatcher, and separate command functions that accept parameters and flags. The CLI also includes a guide
- Messages and errors have now been separated from the code and stored in their own separate file. Utilities function to display info messages or confirmations have been implemented, as well as a few basic custom exceptions
- QoL improvements: 
    - hidden password input (not everywhere just yet!) 
    - Pylerpro now asks to save an open vault before creating a new one or loading another existing one
    - other minor fixes

v0.3
Started logging changes as of this version.
This version implements encryption/decryption of vaults.
