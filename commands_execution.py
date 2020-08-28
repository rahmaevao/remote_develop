"""
This script launches executable files of the remote machine, with the transfer of graphics via ssh.
For working you must pass the label command to the script as an argument.
"""
import subprocess
from constants import USER_AND_ADDRESS, PORT, command_groups
import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Label', nargs='?')
    namespace = parser.parse_args()

    # This magic string will spoil the keys every time.
    # See https://superuser.com/questions/806637/xauth-not-creating-xauthority-file/807112#807112.

    if namespace.Label:
        for this_command_group in command_groups:

            if namespace.Label == this_command_group.label:
                if this_command_group.gui_flag:
                    header = 'ssh -X ' + USER_AND_ADDRESS + ' -p ' + PORT + ' "' + \
                        'xauth list $DISPLAY > temp_list_of_xauth.txt; ' + \
                        'while IFS= read -r line; do export THIS_AUTH=$line; done < temp_list_of_xauth.txt; ' + \
                        'rm temp_list_of_xauth.txt; ' + \
                        'sudo xauth add $THIS_AUTH; '
                else:
                    header = 'ssh ' + USER_AND_ADDRESS + ' -p ' + PORT + ' "'

                for this_command in this_command_group.commands:
                    header += this_command + '; '
                
                header += '"'
                subprocess.call(header, shell=True)
                sys.exit(0)

        print('😕 Unknown command line argument')
        sys.exit(1)
    
    print('😠 Use command line arguments')
    sys.exit(2)
