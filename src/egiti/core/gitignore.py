import logging as lg
from pathlib import Path
from typing import Literal


class GitignoreManager:
    def __init__(self) -> None:
        self.logger = lg.getLogger('egiti.manager')
        self.path: Path | None = None
    

    def init_gitignore_file(self, path: Path, entries: list[str]) -> None:
        self.logger.info('initializing a new .gitignore file')

        if not path:
            path = self.path

        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text('\n'.join(entries) + ('\n' if entries else ''))
        
        self.logger.info(f'.gitignore file successfully initialized in {path}')


    def get_entries(self, comments: bool) -> list[str]:
        self._check_gitignore_file()
        self.logger.info(f'getting entries (comments={comments})')

        entries_raw = self._get_entries_raw()
        entries = []

        for line_n, raw_line in enumerate(entries_raw, start=1):
            line = raw_line.strip()

            if not line:
                self.logger.debug(f'skipping blank line at {line_n}')
                continue

            if line.startswith('#') and not comments:
                self.logger.debug(f'skipping comment at {line_n}')
                continue

            self.logger.debug(f'got entry: \'{line}\'')
            entries.append(line)
        
        return entries
    

    def add_entries(self, adding_entries: list[str], force: bool):
        self._check_gitignore_file()
        self.logger.info('adding new entries')

        # processing adding_entries
        self.logger.debug('removing duplicates from adding_entries')
        adding_entries = list(dict.fromkeys(adding_entries))

        self.logger.debug('stripping all entries from adding_entries')
        adding_entries = [a_e.strip() for a_e in adding_entries]

        # getting current entries
        current_entries = self.get_entries(comments=False)

        # checking for new entries
        new_entries = []

        for adding_entry in adding_entries:
            if (adding_entry not in current_entries) or force:
                new_entries.append(adding_entry)
            
            else:
                self.logger.warning(f'entry \'{adding_entry}\' already exists')
                add_anyways = input('add it anyways? (y/N): ').strip().lower() == 'y'

                if add_anyways:
                    new_entries.append(adding_entry)
                
                else:
                    self.logger.warning(f'skipping already existing entry: \'{adding_entry}\'')
        
        # adding new entries to file
        self._write_entries(new_entries, mode='a')
    

    def remove_entries(self, removing_entries: list[str], force: bool):
        self._check_gitignore_file()
        self.logger.info('removing entries')

        # processing removing_entries
        self.logger.debug('removing duplicates from removing_entries')
        removing_entries = list(dict.fromkeys(removing_entries))

        self.logger.debug('stripping all entries from removing_entries')
        removing_entries = [a_e.strip() for a_e in removing_entries]

        # getting current entries
        current_entries = self._get_entries_raw()

        # removing unexisting removing_entries
        entries_delta = [r_e for r_e in removing_entries
                 if r_e not in [e.strip() for e in current_entries]]
        self.logger.warning(
            "the following entries was not found, "
            f"so will not be removed: {', '.join(entries_delta)}"
        )

        removing_entries = [r_e for r_e in removing_entries if r_e not in entries_delta]

        # collecting new entries
        new_entries = []

        for current_entry in current_entries:
            if current_entry.strip() not in removing_entries:
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
    

    # protected methods
    def _write_entries(self, entries: list[str], mode: Literal['a', 'w']) -> None:
        self.logger.debug(f'writing entries (mode={mode})')

        current_text = self.path.read_text(encoding='utf-8')
        endswith_newline = current_text.endswith('\n')

        with self.path.open(mode=mode, encoding='utf-8') as file:
            if current_text.strip() and not endswith_newline:
                file.write('\n')
            
            file.write('\n'.join(entries) + '\n')
    

    def _get_entries_raw(self) -> None:
        return self.path.read_text(encoding='utf-8').split('\n')


    def _check_gitignore_file(self):
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
