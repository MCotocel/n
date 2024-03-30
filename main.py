#!/usr/bin/env python
# A program wrapping various commands in the NixOS environment

import sys
import subprocess
import socket
import os

class colors:
    CYAN = '\033[96m' # For general messages
    GREEN = '\033[92m' # For sucesses
    YELLOW = '\033[93m' # For warnings
    RED = '\033[91m' # For errors
    END = '\033[0m' # To remove colouring

user = "matei"
config = "/home/" + user + "/nixdots" # Config file location, to be exposed in a configuration file
log_path = "/home/" + user + "/.cache/n.log"
log = open(log_path, "a") # Log file location

# Define command help information
commands = {
    "rebuild": {
        "description": "Switch to a configuration and set it as default in the boot menu",
        "args": "[hostname] - Select host to rebuild"
    },
}

if len(sys.argv) < 2: # Checks if the only argument is the script name
    print(colors.CYAN + "n" + colors.END + " - A wrapper for NixOS commands")
    print("")
    for command, info in commands.items():
        args_with_highlight = info['args'].replace('[', colors.END + colors.YELLOW + '[').replace(']', ']' + colors.END)
        print(colors.GREEN + command + colors.END)
        print("")
        print(f"    {command} {args_with_highlight}")
        print("")
        print(f"    {info['description']}")
        print("")
elif str(sys.argv[1]) == "rebuild": # Logic for rebuilding a configuration
    if len(sys.argv) < 3:
        try:
            os.setuid(0) # Makes sure script can elevate permissions
        except Exception as e:
            print(colors.RED + str(e) + "Elevated permissions are required to rebuild configuration - Exiting..." + colors.END) # Errors out when not running as root
            sys.exit(1)
        print(colors.CYAN + "Rebuilding " + socket.gethostname() + colors.END)
        try:
            os.chmod(log_path, 0o666)  # Read and write permissions for all users
            process = subprocess.Popen(["nixos-rebuild", "--flake", config, "--impure", "switch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Rebuilds config
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                log.write(stdout.decode('utf-8'))
                print(colors.GREEN + "Rebuild finished!" + colors.END)
            else:
                log.write(stderr.decode('utf-8'))
                print(colors.RED + "An error occurred. Check the logs for more information" + colors.END)
        except Exception as e:
            print(colors.RED + "An error occurred: " + str(e) + colors.END)
else: # Argument that doesn't exist
    print(colors.RED + "Argument not recognised. Run "  + colors.END + colors.YELLOW + "n help " + colors.END + colors.RED + "to see all options")
