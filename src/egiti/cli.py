import logging as lg
import sys
from argparse import ArgumentParser, Namespace
from itertools import chain
from pathlib import Path

from egiti.core.gitignore import GitignoreManager
from egiti.core.templates import TemplatesManager
from egiti.utils.logger import setup_logger


def init_argument_parser():
    argument_parser = ArgumentParser(
        description='A utility for easily managing gitignore files',
        epilog='GitHub: https://github.com/wandderq/egiti'
    )

    # global arguments
    argument_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose mode',
    )

    argument_parser.add_argument(
        '-i', '--input',
        type=Path,
        default=Path.cwd() / '.gitignore',
        dest='gitignore_path',
        metavar='PATH',
        help="Path to .gitignore file"
    )

    # egiti [command]
    subparsers = argument_parser.add_subparsers(
        dest='command',
        help='Available commands'
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
        default=[],
        help='Load templates into the new .gitignore'
    )

    init_parser.add_argument(
        '-e', '--entries',
        type=str,
        nargs='+',
        dest='init_entries',
        default=[],
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

    load_parser.add_argument(
        '-f', '--force',
        action='store_true',
        dest='load_force',
        help='Force load'
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

    return argument_parser


class EGITICLI:
    def __init__(self) -> None:
        self.argument_parser = init_argument_parser()

        self.gitignore_manager = GitignoreManager()
        self.templates_manager = TemplatesManager()
        

    def run(self):
        # parsing arguments
        args = self.argument_parser.parse_args()

        # setting up logger
        setup_logger(verbose=args.verbose)
        logger = lg.getLogger('egiti.cli')
        logger.debug('debug mode enabled')

        # setting self.gitignore_manager.path
        self.gitignore_manager.path = args.gitignore_path

        # running command
        match args.command:
            case "init":
                self.run_init(args)
            
            case "status":
                logger.error("WIP")
            
            case "add":
                self.run_add(args)
            
            case "rm":
                self.run_rm(args)
            
            case "load":
                self.run_load(args)
            
            case "show":
                logger.error("WIP")
            
            case _:
                self.argument_parser.print_help()
    
    
    def run_init(self, args: Namespace):
        templates = [
            self.templates_manager.get_template(t_name)
            for t_name in args.init_templates
        ]
        templates_entries = list(chain.from_iterable(templates))

        self.gitignore_manager.init_gitignore_file(
            path=args.init_path,
            entries=args.init_entries + templates_entries
        )
    

    def run_add(self, args: Namespace):
        self.gitignore_manager.add_entries(
            adding_entries=args.add_entries,
            force=args.add_force
        )
    

    def run_rm(self, args: Namespace):
        self.gitignore_manager.remove_entries(
            removing_entries=args.rm_entries,
            force=args.rm_force
        )
    

    def run_load(self, args: Namespace):
        templates = [
            self.templates_manager.get_template(t_name)
            for t_name in args.load_templates
        ]
        templates_entries = list(chain.from_iterable(templates))

        self.gitignore_manager.add_entries(
            adding_entries=templates_entries,
            force=args.load_force
        )
    

def run_cli():
    app = EGITICLI()
    return app.run()

if __name__ == '__main__':
    sys.exit(run_cli())
