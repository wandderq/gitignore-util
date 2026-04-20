import logging as lg
import sys
from pathlib import Path
from typing import Literal


class GitignoreManager:
    def __init__(self, filepath: str) -> None:
        self.logger = lg.getLogger('gitignore.manager')

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
