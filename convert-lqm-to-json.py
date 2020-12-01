from argparse import ArgumentParser
from glob import iglob
from html.parser import HTMLParser
from json import dump, loads
from pathlib import Path
from sys import exit
from zipfile import ZipFile

class NoteParser(HTMLParser):
    def feed(self, data):
        self.lines = []
        HTMLParser.feed(self, data)

    def handle_data(self, data):
        self.lines.append(data)

args_parser = ArgumentParser(description='Convert LG QuickMemo+ export into single, text-only JSON file')
args_parser.add_argument('directory', help='Path to directory that contains .lqm files', type=str)
args = args_parser.parse_args()

directory_path = Path(args.directory).resolve()

if not directory_path.exists():
    exit(f'Path {directory_path} does not exist')

if not directory_path.is_dir():
    exit(f'Path {directory_path} is not a directory')

note_parser = NoteParser()
notes = []

for file_path in iglob(str(Path(f'{directory_path}/*.lqm').resolve())):
    with ZipFile(file_path, 'r') as zip_file:
        with zip_file.open('memoinfo.jlqm') as json:
            data = loads(json.read())
            note_parser.feed(data['Memo']['Desc'])
            notes.append({
                'created_time': data['Memo']['CreatedTime'],
                'modified_time': data['Memo']['ModifiedTime'],
                'text': '\n'.join(note_parser.lines)
            })

notes_count = len(notes)

if notes_count == 0:
    exit(f'No notes found in directory {directory_path}')

file_path = Path(f'{directory_path}/notes.json').resolve()

with open(file_path, 'w') as json_file:
    dump(notes, json_file, indent=2)

print(f"JSON file containing {notes_count} note{'s' if notes_count > 1 else ''} created at {file_path}")
