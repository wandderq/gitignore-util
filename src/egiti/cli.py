import logging as lg
from argparse import ArgumentParser
from pathlib import Path

from egiti._logger import setup_logger
from egiti.core import GitignoreManager
from egiti.template_loader import GITIGNORE_TEMPLATES, load_template


class EGITICLI:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser(
            description='A utility for easily managing gitignore files',
            epilog='GitHub: https://github.com/wandderq/egiti'
        )
        
        # global arguments
        self.argument_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose mode',
        )

        self.argument_parser.add_argument(
            '-i', '--input',
            type=Path,
            default=Path.cwd() / '.gitignore',
            dest='gitignore_path',
            metavar='PATH',
            help="Path to .gitignore file"
        )

        # egiti [command]
        subparsers = self.argument_parser.add_subparsers(
            dest='command',
            help='Available commands',
            required=True,
        )
        
        # egiti init
        init_parser = subparsers.add_parser(
            'init',
            help='Initialize a new .gitignore file'
        )

        init_parser.add_argument(
            'init_path',
            type=Path,
            nargs='?',
            help='Path to the .gitignore file (overrides --input)'
        )

        init_parser.add_argument(
            '-t', '--templates',
            type=str,
            nargs='+',
            dest='init_templates',
            help='Load templates into the new .gitignore'
        )

        init_parser.add_argument(
            '-e', '--entries',
            type=str,
            nargs='+',
            dest='init_entries',
            help='Add entries to the new .gitignore'
        )

        # egiti status
        status_parser = subparsers.add_parser(  # noqa: F841
            'status',
            help='Show current project status based on .gitignore'
        )

        # egiti add
        add_parser = subparsers.add_parser(
            'add',
            help='Add a new entry'
        )

        add_parser.add_argument(
            'add_entries',
            type=str,
            nargs='+',
            help='Entry'
        )

        add_parser.add_argument(
            '-f', '--force',
            action='store_true',
            dest='add_force',
            help='Force add'
        )

        # egiti rm
        rm_parser = subparsers.add_parser(
            'rm',
            help='Remove an entry'
        )

        rm_parser.add_argument(
            'rm_entries',
            type=str,
            nargs='+',
            help='Entry'
        )

        rm_parser.add_argument(
            '-f', '--force',
            action='store_true',
            dest='rm_force',
            help='Force removal'
        )

        # egiti load
        load_parser = subparsers.add_parser(
            'load',
            help='Load .gitignore templates'
        )

        load_parser.add_argument(
            'load_templates',
            type=str,
            nargs='+',
            help='Template names'
        )

        # egiti show
        show_parser = subparsers.add_parser(
            'show',
            help='Show contents'
        )

        show_parser.add_argument(
            '-c', '--comments',
            action='store_true',
            dest='show_comments',
            help='Show with comments'
        )
        

    def run(self) -> int:
        # parsing arguments
        args = self.argument_parser.parse_args()

        # setting up logger
        setup_logger(verbose=args.verbose)
        logger = lg.getLogger('egiti.cli')

        logger.debug('Debug mode enabled')


def run_cli():
    app = EGITICLI()
    return app.run()
        
