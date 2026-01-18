from argparse import ArgumentParser, Namespace
from .template_loader import GITIGNORE_TEMPLATES, load_template
from typing import Literal
from pathlib import Path

import colorlog as clg
import logging as lg
import sys
import os


root_logger = lg.getLogger('gitignore')
root_logger.handlers.clear()
root_logger.setLevel(lg.INFO)

stream_handler = lg.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(clg.ColoredFormatter(
    fmt="{log_color}[{name}@{levelname}]: {message}{reset}",
    style='{',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red'
    }
))

root_logger.addHandler(stream_handler)


class GitignoreManager:
    def __init__(self, filepath: str) -> None:
        self.logger = lg.getLogger('gitignore.manager')

        self.path = Path(filepath)
        if self.path.is_dir():
            self.path /= '.gitignore'
        self.path = self.path.absolute()

        if not self.path.exists():
            self.logger.warning(f'{self.path} not found')
            create = not input('create it? (default: y) (y/n): ').strip().lower() in ['n', 'no']

            if create:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.touch()
            
            else:
                self.logger.error(f'{filepath} not found')
                sys.exit(1)
        

    def get_entries(self, with_comments: bool = False) -> list:
        with open(self.path, 'r', encoding='utf-8') as file:
            entries = []

            for line in file:
                line = line.strip()
                if not line: continue

                if with_comments or not line.startswith('#'):
                    entries.append(line)

        
        return entries
    

    def add_entries(self, new_entries: list, mode: Literal['a', 'w'] = 'a') -> None:
        with open(self.path, 'r', encoding='utf-8') as file:
            raw_file_lines = file.readlines()
            file_lines = [l.strip() for l in raw_file_lines]

        with open(self.path, mode, encoding='utf-8') as file:
            if mode == 'a' and raw_file_lines and not raw_file_lines[-1].endswith('\n'):
                file.write('\n')
            
            for entry in new_entries:
                if not entry in file_lines:
                    file.write(entry + '\n')
                    self.logger.debug(f'entry added: {entry}\\n')
                
                else:
                    self.logger.warning(f'entry alreday exists: {entry}')
    

    def remove_entries(self, rm_entries: list) -> None:
        old_entries = self.get_entries()
        new_entries = [e for e in old_entries if not e in rm_entries]
        self.logger.info(f'removed entries: {len(old_entries)-len(new_entries)}')

        with open(self.path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_entries) + '\n')


class GitignoreCLI:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser(
            description='Quick editor for .gitignore files',
            epilog='GitHub: https://github.com/wandderq/gitignore-util'
        )

        subparsers = self.argument_parser.add_subparsers(
            dest='command',
            metavar='[command]',
            help='command to do'
        )

        add_parser = subparsers.add_parser('add', help='add new entries to .gitignore')
        add_parser.add_argument('entries', nargs='+', help='entries to add, e.g.: gitignore add .vscode .venv')
        add_parser.add_argument('-m', '--mode', choices=['a', 'w'], default='a', help='write mode. default: append')

        rm_parser = subparsers.add_parser('rm', help='remove entries from .gitignore')
        rm_parser.add_argument('entries', nargs='+', help='entries to remove, e.g.: gitignore rm .python-version')

        show_parser = subparsers.add_parser('show', help='display all entries from .gitignore')
        show_parser.add_argument('-a', '--all', action='store_true', help='include comments in the output')
        show_parser.add_argument('-t', '--templates', action='store_true', help='show available templates')

        load_parser = subparsers.add_parser('load', help='load .gitignore templates from https://github.com/github/gitignore')
        load_parser.add_argument('templates', nargs='+', help='templates to load, see gitignore show -t')
        load_parser.add_argument('-a', '--all', action='store_true', help='load with comments')

        self.argument_parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
        self.argument_parser.add_argument('-i', '--input-file', default='.gitignore', help='.gitignore filepath, default: .gitignore')



    def run(self) -> None | int:
        args = self.argument_parser.parse_args()
        if args.verbose: root_logger.setLevel(lg.DEBUG)
        logger = lg.getLogger('gitignore.cli')
        
        manager = GitignoreManager(str(args.input_file).strip())

        if args.command in ['add', 'rm']:
            args_entries = list(set(args.entries))


        if args.command == 'add':
            manager.add_entries(args_entries, args.mode)
            logger.info('Done!')
        

        elif args.command == 'rm':
            manager.remove_entries(args_entries)
            logger.info('Done!')

        
        elif args.command == 'show':
            if not args.templates:
                entries = manager.get_entries(with_comments=args.all)
                for i, entry in enumerate(entries, start=1):
                    color = '\033[0m' if entry.startswith('#') else '\033[32m'
                    print(f'{color}{i}: {entry}\033[0m', flush=True)
            
            else:
                print(f"available templates: {', '.join(GITIGNORE_TEMPLATES.keys())}")


        elif args.command == 'load':
            for template_name in args.templates:
                logger.info(f'Loading template: {template_name}')
                entries = load_template(template_name, with_comments=args.all)
                manager.add_entries(entries, mode='a')

        
        else:
            self.argument_parser.print_help()
        

def run_cli():
    # try:
        app = GitignoreCLI()
        return app.run()
    
    # except Exception as e:
    #     root_logger.error(f'error: {str(e)}. cause: {str(e.__cause__)}')
        
