import logging as lg
import sys
from functools import wraps
from pathlib import Path
from typing import Literal


class GitignoreManager:
    def __init__(self, gitignore_path: Path) -> None:
        self.logger = lg.getLogger('egiti.manager')
        self.path = gitignore_path
    

    @staticmethod
    def check_gitignore_file(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.logger.debug(f'checking .gitignore file: {self.path}')

            if self.path.is_dir(): self.path /= '.gitignore'

            if not self.path.exists():
                self.logger.error('the .gitignore file not found')
                create = input('create a new empty .gitignore? (Y/n): ').strip().lower() != 'n'

                if create:
                    self.init_gitignore_file(self.path, [])

                else:
                    raise FileNotFoundError('The .gitignore file not found!')
            
            self.path = self.path.absolute()
            return func(self, *args, **kwargs)
        
        return wrapper
    

    def init_gitignore_file(self, path: Path, entries: list[str]) -> None:
        self.logger.info('initializing a new .gitignore file')

        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

        path.write_text('\n'.join(entries) + '\n')
        
        self.logger.info(f'.gitignore file successfully initialized in {path}')
    
    
    def _write_entries(self, entries: list[str], mode: Literal['a', 'w']) -> None:
        self.logger.debug(f'writing entries (mode={mode})')

        current_text = self.path.read_text(encoding='utf-8')
        endswith_newline = current_text.endswith('\n')

        with self.path.open(mode=mode, encoding='utf-8') as file:
            if not endswith_newline:
                file.write('\n')
            
            file.write('\n'.join(entries) + '\n')


    @check_gitignore_file
    def get_entries(self, comments: bool) -> list[str]:
        self.logger.debug(f'getting entries (comments={comments})')

        entries = []
        with open(self.path, encoding='utf-8') as gitignore_file:
            for line_n, line in enumerate(gitignore_file, start=1):
                line = line.strip()

                if not line:
                    self.logger.debug(f'skipping blank line at {line_n}')
                    continue

                if line.startswith('#') and not comments:
                    self.logger.debug(f'skipping comment at {line_n}')
                    continue

                self.logger.debug(f'adding entry: \'{line}\'')
                entries.append(line)
        
        return entries
    

    @check_gitignore_file
    def add_entries(self, entries: list[str], force: bool):
        self.logger.info('adding new entries')
        current_entries = self.get_entries(comments=False)
        new_entries = []

        for entry in entries:
            if (entry not in current_entries) or force:
                new_entries.append(entry)
            
            else:
                self.logger.warning(f'entry \'{entry}\' alreday exists')
                add_anyways = input('add it anyways? (y/N): ').strip().lower() == 'y'

                if add_anyways:
                    new_entries.append(entry)
                
                else:
                    self.logger.warning(f'skipping alreday existing entry: \'{entry}\'')
        
        self._write_entries(new_entries, mode='a')
    

    @check_gitignore_file
    def remove_entries(self, entries: list[str], force: bool):
        self.logger.info('removing entries')

        current_entries = self.get_entries(comments=False)
        new_entries = []

        entries_delta = [e for e in entries if e not in current_entries]
        self.logger.warning(
            "the following entries was not found, "
            f"so will not be removed: {', '.join(entries_delta)}"
        )

        for current_entry in current_entries:
            if current_entry not in entries:
                new_entries.append(current_entry)
                continue
            
            else:
                if force or input(
                            f'are you sure about removing \'{current_entry}\'? (y/N): '
                            ).strip().lower() == 'y':
                    continue

                else:
                    new_entries.append(current_entry)
        
        self._write_entries(new_entries, mode='w')


        
        

class GitignoreManager_old:
    def __init__(self, filepath: str) -> None:
        self.logger = lg.getLogger('egi.manager')

        self.path = Path(filepath)
        if self.path.is_dir():
            self.path /= '.gitignore'
        self.path = self.path.absolute()

        if not self.path.exists():
            self.logger.warning(f'{self.path} not found')
            create = input('create it? (default: y) (y/n): ').strip().lower() \
                not in ['n', 'no']

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
            file_lines = [line.strip() for line in raw_file_lines]

        with open(self.path, mode, encoding='utf-8') as file:
            if mode == 'a' and raw_file_lines and not raw_file_lines[-1].endswith('\n'):
                file.write('\n')
            
            for entry in new_entries:
                if entry not in file_lines:
                    file.write(entry + '\n')
                    self.logger.debug(f'entry added: {entry}\\n')
                
                else:
                    self.logger.warning(f'entry alreday exists: {entry}')
    

    def remove_entries(self, rm_entries: list) -> None:
        old_entries = self.get_entries()
        new_entries = [e for e in old_entries if e not in rm_entries]
        self.logger.info(f'removed entries: {len(old_entries)-len(new_entries)}')

        with open(self.path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_entries) + '\n')
