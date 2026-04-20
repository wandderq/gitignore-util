from argparse import ArgumentParser
from egiti.template_loader import GITIGNORE_TEMPLATES, load_template
from egiti.core import GitignoreManager

import colorlog as clg
import logging as lg
import sys


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


class EGITICLI:
    def __init__(self) -> None:
        self.argument_parser = ArgumentParser(
            description='A utility for easily managing gitignore files ',
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
        if args.verbose:
            root_logger.setLevel(lg.DEBUG)
        
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
                if not template_name in GITIGNORE_TEMPLATES:
                    logger.error(f'Template not found: {template_name}')
                    continue

                logger.info(f'Loading template: {template_name}')
                entries = load_template(template_name, with_comments=args.all)
                manager.add_entries(entries, mode='a')

        
        else:
            self.argument_parser.print_help()
        

def run_cli():
    try:
        app = EGITICLI()
        return app.run()
    
    except Exception as e:
        root_logger.error(f'error: {str(e)}. cause: {str(e.__cause__)}')
        
