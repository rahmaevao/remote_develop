"""
This script is designed to work with a virtual machine

This script is able to prepare the environment for working with the code that is on the virtual machine.
Also, this script safely shuts down the virtual machine.

Пример работы:

1. Run the virtual machine and mount code directory
vbox.py run

2. Shutting down the virtual machine
vbox.py poweroff
"""

import subprocess
import sys
from constants import USER_AND_ADDRESS, PORT, MOUNT_PATH, SOURCE_CODE_PATH, NAME_VIRTUAL_MACHINE_IMG
import datetime
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?')
    namespace = parser.parse_args()

    if namespace.command is None:
        print('😠 Use the command line arguments')
        sys.exit(1)

    if namespace.command == 'run':
        # TODO: Добавить проверку на наличие пакетов VirtualBox, ssh, sudo apt install ssh-tools, sshfs

        # Checking if VirtualBox has an image of the required machine
        out = subprocess.Popen("VBoxManage list vms",
                               shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if out.find(NAME_VIRTUAL_MACHINE_IMG) == -1:
            print(
                '😠 Required viral machine not found. Add virtual machine image into VirtualBox')
            sys.exit(-1)
        else:
            print('👍 Virtual machine image found')

        # Checking if the machine is currently running or not
        out = subprocess.Popen("VBoxManage list runningvms",
                               shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if out.find(NAME_VIRTUAL_MACHINE_IMG) != -1:
            print('😒 The virtual machine is already running')
        else:
            subprocess.call("VBoxManage startvm '" +
                            NAME_VIRTUAL_MACHINE_IMG + "' --type headless", shell=True)

        # Waiting for full load
        TIMEOUT = 100  # s
        loaded = False
        t0 = datetime.datetime.now()
        while (datetime.datetime.now() - t0).seconds < TIMEOUT:
            out = subprocess.Popen('ssh-ping -c 1 -p ' + PORT + ' ' + USER_AND_ADDRESS,
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            if out.find('Pong') != -1:
                loaded = True
                break
        if loaded:
            print('👍 Machine is loaded')
        else:
            print('😠 Machine is not loaded')

        # Mount disk via ssh
        subprocess.call('umount ' + MOUNT_PATH,
                        shell=True, stderr=subprocess.PIPE)
        subprocess.call('rm -rf ' + MOUNT_PATH, shell=True)
        subprocess.call('mkdir ' + MOUNT_PATH, shell=True)
        subprocess.call('sshfs -o allow_other ' + USER_AND_ADDRESS + ':' +
                        SOURCE_CODE_PATH + ' ' + MOUNT_PATH + ' -p' + PORT, shell=True)

        # Checking for mount
        out = subprocess.Popen('ls ' + MOUNT_PATH,
                               shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if len(out) == 0:
            print('😠 Mounting is not correct')
        else:
            print('👍 Mounting is correct')
        sys.exit(0)

    if namespace.command == 'poweroff':
        out = subprocess.Popen("vboxmanage list runningvms",
                               shell=True,
                               stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        if out.find(NAME_VIRTUAL_MACHINE_IMG) == -1:
            print("🤦‍ Mate, the machine hasn't even started...")
            sys.exit(-1)

        subprocess.call('ssh ' + USER_AND_ADDRESS + ' -p ' + PORT + " '" +
                        'sudo poweroff' +
                        "'",
                        shell=True)
        print('✋ The virtual machine is turned off. Did a good job today. 🛌')
        sys.exit(0)

    print('😕 Unknown command line argument')
