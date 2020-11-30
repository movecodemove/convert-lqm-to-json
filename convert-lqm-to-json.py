from argparse import ArgumentParser
from glob import iglob
from html2text import html2text
from json import dump, loads
from pathlib import Path
from re import sub
from zipfile import ZipFile

parser = ArgumentParser(description='Convert LG QuickMemo+ export into single text-only JSON file')
parser.add_argument('directory', help='Path to directory that contains .lqm files', type=str)

args = parser.parse_args()
directory_path = Path(args.directory).resolve()

if directory_path.exists() and directory_path.is_dir():
    notes = []

    for file_path in iglob(str(Path(f'{directory_path}/*.lqm').resolve())):
        with ZipFile(file_path, 'r') as zip_file:
            with zip_file.open('memoinfo.jlqm') as json:
                data = loads(json.read())
                notes.append({
                    'created_time': data['Memo']['CreatedTime'],
                    'modified_time': data['Memo']['ModifiedTime'],
                    'text': sub(r'\n\s*\n', '\n', html2text(data['Memo']['Desc'])).strip()
                })

    with open(str(Path(f'{directory_path}/notes.json').resolve()), 'w') as json_file:
        dump(notes, json_file, indent=2)
