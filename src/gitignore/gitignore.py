from argparse import ArgumentParser
from pathlib import Path

import sys
import os


class Gitignore:
    def __init__(self) -> None:
        self.arg_parser = ArgumentParser(
            description='.gitignore fast redactor'
        )
        
        subparsers = self.arg_parser.add_subparsers(
            dest='command',
            required=True,
            metavar='[command]'
        )
        
        add_parser = subparsers.add_parser(
            'add',
            help='add new line to the .gitignore'
        )
        add_parser.add_argument(
            'lines',
            nargs='+',
            help='lines to add, ex.: gitignore add .vscode .venv'
        )
        
        show_parser = subparsers.add_parser(
            'show',
            help='shows all lines from .gitignore'
        )
    
    
    
    def run(self) -> None | int:
        args = self.arg_parser.parse_args()
        
        gitignore_file = Path('.gitignore')
        if not gitignore_file.exists():
            print(f'\033[31m.gitignore not found in {os.getcwd()}\033[0m')
            create = input('create it? (default: n) (y/n): ').strip().lower() in ['y', 'ye', 'yes', '1']
            if create:
                gitignore_file.touch()
            
            else:
                return 1
        
        
        if args.command == 'add':
            with open(gitignore_file.absolute(), 'r', encoding='utf-8') as file:
                raw_file_lines = file.readlines()
                
                # getting lines from args and from file:
                file_lines = [file_line.strip() for file_line in raw_file_lines if file_line.strip() and not file_line.strip().startswith('#')]
                args_lines = list(set([arg_line.strip() for arg_line in args.lines]))
                
                # checking if file endswith \n
                last_line = raw_file_lines[-1]
                set_newline = last_line.strip() and not last_line.endswith('\n')
            
            
            with open(gitignore_file.absolute(), 'a', encoding='utf-8') as file:
                if set_newline:
                    file.write('\n')
                
                for line in args_lines:
                    if not line in file_lines:
                        file.write(line + '\n')
                        print(f'\033[32mLine added: {line}')
                    
                    else:
                        print(f'\033[33mLine alreday exists: {line}')
                
                return 0


def run_cli():
    app = Gitignore()
    ec = app.run()
    sys.exit(ec if ec is not None else 0)