from argparse import ArgumentParser, Namespace
from pathlib import Path

import sys
import os


class Gitignore:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser(
            description='Quick editor for .gitignore files',
            epilog='GitHub: https://github.com/wandderq/gitignore-util'
        )

        subparsers = self.argument_parser.add_subparsers(
            dest='command',
            metavar='[command]'
        )

        add_parser = subparsers.add_parser(
            'add',
            help='add new entries to .gitignore'
        )
        add_parser.add_argument(
            'lines',
            nargs='+',
            help='entries to add, e.g.: gitignore add .vscode .venv'
        )

        show_parser = subparsers.add_parser(
            'show',
            help='display all entries from .gitignore'
        )
        show_parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='include comments in the output'
        )

        rm_parser = subparsers.add_parser(
            'rm',
            help='remove entries from .gitignore'
        )
        rm_parser.add_argument(
            'lines',
            nargs='+',
            help='entries to remove, e.g.: gitignore rm .python-version'
        )
    
    
    def add_lines(self, gitignore_file: Path, args: Namespace) -> int:
        with open(gitignore_file, 'r', encoding='utf-8') as file:
            raw_file_lines = file.readlines()
            
            # getting lines from args and from file
            file_lines = [file_line.strip() for file_line in raw_file_lines if file_line.strip() and not file_line.strip().startswith('#')]
            args_lines = list(set([arg_line.strip() for arg_line in args.lines]))
            
            # checking if file endswith \n
            last_line = raw_file_lines[-1]
            set_newline = last_line.strip() and not last_line.endswith('\n')
        
            
        with open(gitignore_file, 'a', encoding='utf-8') as file:
            # writing \n
            if set_newline:
                file.write('\n')
            
            # adding new lines only if they are not exist
            for line in args_lines:
                if not line in file_lines:
                    file.write(line + '\n')
                    print(f'\033[32mLine added: {line}')
                
                else:
                    print(f'\033[33mLine alreday exists: {line}')
            
            return 0
    
    
    def show_lines(self, gitignore_file: Path, args: Namespace) -> int:
        with open(gitignore_file, 'r', encoding='utf-8') as file:
            # getting lines from file
            lines = [
                (file_line.strip(), i)
                for i, file_line in enumerate(file.readlines(), start=1)
                if file_line.strip()
            ]
            
            for line, i in lines:
                is_comment = line.startswith('#')
                if not is_comment or args.all:
                    color = '\033[32m' if not is_comment else '\033[0m'
                    print(f'{color}.gitignore:{i}:\033[0m {line}')
        
        return 0
   
   
    def rm_lines(self, gitignore_file: Path, args: Namespace) -> int:
        with open(gitignore_file, 'r', encoding='utf-8') as file:
            file_content = [file_line.strip() for file_line in file.readlines()]
            args_lines = list(set([arg_line.strip() for arg_line in args.lines]))
            
            for arg_line in args_lines:
                if arg_line in file_content:
                    file_content.remove(arg_line)
                    print(f'Removed: {arg_line}')
                
                else:
                    print(f'Line {arg_line} doesn\'t exist in .gitignore')
        
        
        with open(gitignore_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(file_content))
        
        
        return 0
    
    
    def get_gitignore_file(self) -> Path | None:
        gitignore_file = Path('.gitignore')
        
        if not gitignore_file.exists():
            print(f'\033[31m.gitignore not found in {os.getcwd()}\033[0m')
            create = input('Create it? (default: n) (y/n): ').strip().lower() in ['y', 'ye', 'yes', '1']
            if create:
                gitignore_file.touch()
            
            else:
                return
        
        return gitignore_file.absolute()
   
            
    def run(self) -> None | int:
        args = self.argument_parser.parse_args()
        
        gitignore_file = self.get_gitignore_file()
        if gitignore_file is None:
            return 1
        
        
        if args.command == 'add':
            return self.add_lines(gitignore_file, args)
        
        elif args.command == 'show':
            return self.show_lines(gitignore_file, args)
        
        elif args.command == 'rm':
            return self.rm_lines(gitignore_file, args)
        
        else:
            self.argument_parser.print_help()


def run_cli():
    app = Gitignore()
    ec = app.run()
    sys.exit(ec if ec is not None else 0)