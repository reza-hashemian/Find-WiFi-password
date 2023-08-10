#!/usr/bin/env python3
"""With this module you can find all Wi-FI's that you connected with password.

classes:
    FindWifi:
        Find all network wifis with password.

        This class design to find all network that we connect to them with
        password.

        methods:
            __init__():
                This method save all wifi network with its password in
                'wifi_list' attributes.

            print_wifis():
                Print all ssid and password in terminal.

            save(dest_path, mode_file):
                Save content in location of 'dest_path'.
                mode_file:  Is the mode that we want to save file.
                            if we want to if exist this file name
                            clear and then write use 'w', and if
                            we want to append at the end of file
                            should use 'a'. default is 'a'.

        attributes:
            wifi_list (list): list dictionary's that contain 'ssid' and
            'password' of our networks.

"""

import subprocess
import re
from colorama import Fore
from colorama import Style
import shutil
import os

# get terminal size
terminal_size = shutil.get_terminal_size()


class FindeWifi:
    """Find all network wifis with password.

    This class design to find all network that we connect to them with
    password.

    methods:
        __init__():
            This method save all wifi network with its password in
            'wifi_list' attributes.
        print_wifis():
            Print all ssid and password in terminal.
        save(dest_path, mode_file):
            Save content in location of 'dest_path'.
            mode_file:  Is the mode that we want to save file.
                        if we want to if exist this file name
                        clear and then write use 'w', and if
                        we want to append at the end of file
                        should use 'a'. default is 'a'.


    attributes:
        wifi_list (list): list dictionary's that contain 'ssid' and
        'password' of our networks.

    """

    def __init__(self) -> None:
        """Find all networks with its password.

        This method save all wifi network with its password in
        'wifi_list' attributes.
        """
        command_output: str = subprocess.run(
            ['netsh', 'wlan', 'show', 'profiles'],
            shell=True,
            capture_output=True
        ).stdout.decode()

        profile_names: list = re.findall(
            'All User Profile     : (.*)\r',
            command_output
        )

        self.wifi_list: list = list()

        if profile_names:
            for name in profile_names:
                wifi_profile: dict = dict()
                profile_info: str = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', name],
                    shell=True,
                    capture_output=True
                ).stdout.decode()

                if re.search('Security key           : Absent', profile_info):
                    continue
                else:
                    wifi_profile['ssid'] = name
                    profile_info_pass: str = subprocess.run(
                        [
                            'netsh',
                            'wlan',
                            'show',
                            'profile',
                            name,
                            'key=clear'
                        ],
                        shell=True, capture_output=True
                    ).stdout.decode()

                    password = re.search(
                        'Key Content            : (.*)\r',
                        profile_info_pass
                    )

                    if password == None:
                        wifi_profile['password'] = None
                    else:
                        wifi_profile['password'] = password[1]
                    self.wifi_list.append(wifi_profile)

    def print_wifis(self):
        """Print all ssid and password in terminal."""
        print(f"""{Fore.GREEN}{'-' * terminal_size.columns}{Style.RESET_ALL}\n""")
        for item in self.wifi_list:
            print(
                f"""{Fore.RED}ssid of wifi: {Fore.CYAN}{item['ssid']:30}::"""
                f"""\t{Fore.RED}password: {Fore.CYAN}{item['password']}"""
                f"""{Style.RESET_ALL}"""
            )
        print(f"""{Fore.GREEN}{'-' * terminal_size.columns}{Style.RESET_ALL}\n""")

    def save(self, dest_path, mode_file='a'):
        """Save content in file with path 'dest_path'.

        Parameters:
            dest_path (str): The destination of file that we need to
                             save.
            mode_file (str): The mode that we want to save file.
                             if we want to if exist this file name
                             clear and then write use 'w', and if
                             we want to append at the end of file
                             should use 'a'. default is 'a'.
        """
        mode_is_true = mode_file == 'w' or mode_file == 'a'
        exist_path = os.path.exists(dest_path)
        if mode_is_true and exist_path:
            with open(dest_path.removesuffix('\\') + '\\find_wifi_with_pass.txt', mode_file) as f:
                for item in self.wifi_list:
                    f.write(f"""ssid of wifi: {item['ssid']:30}::"""
                            f"""\tpassword: {item['password']}"""
                            f"""\n""")
        else:
            if not exist_path:
                print(f'{Fore.RED} ***path that entered is false{Style.RESET_ALL}')
            if not mode_is_true:
                print(f'{Fore.RED} ***mode file is false{Style.RESET_ALL}')


def create_hello_message():
    special_message = """

888                                             888888b.            888                     
888                                             888  "88b           888                     
888                                             888  .88P           888                     
888      .d88b.   8888b.  888d888 88888b.       8888888K.  888  888 888888 .d88b.  .d8888b  
888     d8P  Y8b     "88b 888P"   888 "88b      888  "Y88b 888  888 888   d8P  Y8b 88K      
888     88888888 .d888888 888     888  888      888    888 888  888 888   88888888 "Y8888b. 
888     Y8b.     888  888 888     888  888      888   d88P Y88b 888 Y88b. Y8b.          X88 
88888888 "Y8888  "Y888888 888     888  888      8888888P"   "Y88888  "Y888 "Y8888   88888P' 
                                                                888                         
                                                           Y8b d88P                         
                                                            "Y88P"                          

    """

    final_special_message = ''
    for item in special_message.split('\n'):
        final_special_message += f'{item:^{terminal_size.columns}}\n'

    hello_message: str = f"""
{'-' * terminal_size.columns}
{'-' * terminal_size.columns}{Fore.GREEN}
{final_special_message}{Style.RESET_ALL}
{'-' * terminal_size.columns}
{'-' * terminal_size.columns}
{'WELCOME TO MY SCRIPT':^{terminal_size.columns}}
{Fore.RED}{'please subscribe to my youtube channel:':^{terminal_size.columns}}
{Fore.CYAN}{'https://www.youtube.com/@learnbytes':^{terminal_size.columns}}{Style.RESET_ALL}

    """
    return hello_message


def main():
    print(create_hello_message())
    message: str = (

        f"""{Fore.BLUE}{'-' * terminal_size.columns}{Style.RESET_ALL}\n"""
        f"""{Fore.CYAN} for continue press 'c'{Style.RESET_ALL}\n"""
        f"""{Fore.CYAN} for exit press 'q'{Style.RESET_ALL}\n"""
        f"""{Fore.GREEN}Enter your choice: {Style.RESET_ALL}\n"""

    )
    while (command := input(message)) != 'q'.lower():
        match command.split():
            case ['c']:
                message: str = (
                    f"""{Fore.BLUE}{'-' * terminal_size.columns}{Style.RESET_ALL}\n"""

                    f"""{Fore.CYAN} for see wifi ssid and password type: 'see'{Style.RESET_ALL}\n"""
                    f"""{Fore.CYAN} for save wifi ssid and password in file type: 'save'{Style.RESET_ALL}\n"""
                    f"""{Fore.CYAN} for exit press 'q'{Style.RESET_ALL}\n"""
                    f"""{Fore.GREEN}Enter your choice: {Style.RESET_ALL}\n"""

                )

            case ['see']:
                FindeWifi().print_wifis()
                message: str = (
                    f"""{Fore.BLUE}{'-' * terminal_size.columns}{Style.RESET_ALL}\n"""

                    f"""{Fore.CYAN} for see wifi ssid and password type: 'see'{Style.RESET_ALL}\n"""
                    f"""{Fore.CYAN} for save wifi ssid and password in file type: 'save'{Style.RESET_ALL}\n"""
                    f"""{Fore.CYAN} for exit press 'q'{Style.RESET_ALL}\n"""
                    f"""{Fore.GREEN}Enter you'r choice: {Style.RESET_ALL}\n"""

                )

            case ['save']:
                while True:
                    message_for_save: str = (
                        f"""{Fore.BLUE}{'-' * terminal_size.columns}{Style.RESET_ALL}\n"""

                        f"""{Fore.CYAN} for save wifi ssid and password in file: {Fore.RED}path_your_location  mode{Style.RESET_ALL}\n"""
                        f"""\t {Fore.RED}path_your_location{Style.RESET_ALL} is required .{Style.RESET_ALL}\n"""
                        f"""\t {Fore.RED}mode{Style.RESET_ALL} is optional:{Style.RESET_ALL}\n"""
                        f"""\t\t if we want to delete file 'fine_wifi_with_pass.txt' if exist 'w'{Style.RESET_ALL}\n"""
                        f"""\t\t if we want to append at the end of file if exist 'a' {Style.RESET_ALL}\n"""
                        f"""\t {Fore.RED}e.x: {Style.RESET_ALL}C:\\Users\\name\\Downloads{Style.RESET_ALL}\n"""
                        f"""\t {Fore.RED}e.x: {Style.RESET_ALL}C:\\Users\\name\\Downloads,  a{Style.RESET_ALL}\n"""
                        f"""\t {Fore.RED}e.x: {Style.RESET_ALL}C:\\Users\\name\\Downloads,  w{Style.RESET_ALL}\n"""
                        f"""{Fore.CYAN} for canceling save file 'cancel'{Style.RESET_ALL}\n"""
                        f"""{Fore.GREEN}Enter your choice: {Style.RESET_ALL}\n"""
                    )
                    user_input = input(message_for_save)

                    match user_input.split(','):

                        case ['cancel']:
                            break

                        case [path, mode]:
                            if not (exist_path := os.path.exists(path.strip())):
                                print(f'{Fore.RED} ***path that entered is false{Style.RESET_ALL}')
                            if not (mode_is_true := (mode.strip() == 'w' or mode.strip() == 'a')):
                                print(f'{Fore.RED} ***mode file is false{Style.RESET_ALL}')
                            if exist_path and mode_is_true:
                                FindeWifi().save(path.strip(), mode.strip())

                            break

                        case [path]:
                            if not os.path.exists(path.strip()):
                                print(f'{Fore.RED} ***ath that entered is false{Style.RESET_ALL}')
                            else:
                                FindeWifi().save(path)
                            break


if __name__ == '__main__':
    main()