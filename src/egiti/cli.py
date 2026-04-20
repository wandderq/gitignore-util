import logging as lg
from argparse import ArgumentParser

from egiti._logger import setup_logger
from egiti.core import GitignoreManager
from egiti.template_loader import GITIGNORE_TEMPLATES, load_template


class EGITICLI:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser(
            description='A utility for easily managing gitignore files ',
            epilog='GitHub: https://github.com/wandderq/gitignore-util'
        )

        subparsers = self.argument_parser.add_subparsers(
            dest='command',
            metavar='[command]',
            help='Available commands',
            required=True
        )

        # global args
        self.argument_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose mode'
        )
        self.argument_parser.add_argument(
            '-i', '--input',
            default='.gitignore',
            help='Gitignore file path (default: .gitignore)'
        )

        # egiti add
        add_parser = subparsers.add_parser(
            'add',
            help='Add new entries to .gitignore'
        )
        add_parser.add_argument(
            'entries',
            nargs='+',
            help='Entries to add (e.g.: egiti add .venv)'
        )
        add_parser.add_argument(
            '-m', '--mode',
            choices=['a', 'w'],
            default='a',
            help='File mode (default: append)'
        )

        # egiti rm
        rm_parser = subparsers.add_parser(
            'rm',
            help='Remove entries from .gitignore'
        )
        rm_parser.add_argument(
            'entries',
            nargs='+',
            help='Entries to remove (e.g.: egiti rm .vscode)'
        )

        # egiti show
        show_parser = subparsers.add_parser(
            'show',
            help='Display all entries from .gitignore'
        )
        show_parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='Include comments in the output'
        )
        show_parser.add_argument(
            '-t', '--templates',
            action='store_true',
            help='Show available templates'
        )

        # egiti load
        load_parser = subparsers.add_parser(
            'load',
            help='Load .gitignore templates'
        )
        load_parser.add_argument(
            'templates',
            nargs='+',
            help='Templates to load (see egiti show -t)'
        )
        load_parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='Load with comments'
        )


    def run(self) -> None | int:
        args = self.argument_parser.parse_args()

        # setting up logger
        setup_logger(verbose=args.verbose)
        logger = lg.getLogger('egiti.cli')

        # loading manager
        manager = GitignoreManager(str(args.input_file).strip())

        # running command
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
                if template_name not in GITIGNORE_TEMPLATES:
                    logger.error(f'Template not found: {template_name}')
                    continue

                logger.info(f'Loading template: {template_name}')
                entries = load_template(template_name, with_comments=args.all)
                manager.add_entries(entries, mode='a')
        

def run_cli():
    app = EGITICLI()
    return app.run()
        
