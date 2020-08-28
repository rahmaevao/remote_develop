import yaml
from dataclasses import dataclass
from os.path import join, dirname, realpath

config_file_path = join(dirname(realpath(__file__)), 'configuration.yml')
with open(config_file_path, encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

PORT = str(config['SSH port'])
USER_AND_ADDRESS = config['User and address']
NAME_VIRTUAL_MACHINE_IMG = config['Name of virtual machine']
MOUNT_PATH = config['Mount point on host system']
SOURCE_CODE_PATH = config['Path source code directory in remote machine']


@dataclass
class CommandGroup:
    label: str
    gui_flag: bool
    commands: list


command_groups = [CommandGroup(this_config['Label'],
                               this_config['GUI [True/False]'],
                               this_config['Commands'])
                  for this_config in config['Command groups']]