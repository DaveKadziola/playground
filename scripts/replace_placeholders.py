# put py and ini in tools folder
# if not set execute command set BASE_PATH=<project-root-dir> | export PATH=<project-root-dir>
import os
import re
import sys

FILE_EXTENSIONS = ('.config', '.json', '.xml', '.bat')

def load_replacements(replace_file):
    replacements = []
    with open(replace_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip lines starting with '--'
            if line and not line.startswith('--'):
                parts = line.split(';', 1)
                if len(parts) == 2:
                    original = parts[0]
                    pattern = re.escape(original)
                    replacements.append((original, re.compile(pattern), parts[1]))
    return replacements

def replace_in_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    for original, pattern, replacement in replacements:
        new_content, count = pattern.subn(replacement, content)
        if count > 0:
            print(f"Replaced '{original}' with '{replacement}' in {file_path} ({count} times)")
            modified = True
        content = new_content

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def process_files():
    BASE_PATH = os.getenv('BASE_PATH')
    if not BASE_PATH:
        print("Error: BASE_PATH environment variable not set", file=sys.stderr)
        sys.exit(1)

    replace_file = os.path.join(BASE_PATH, 'tools', 'replace_placeholders.config')
    if not os.path.exists(replace_file):
        print(f"Error: Replacement file {replace_file} not found", file=sys.stderr)
        sys.exit(1)

    replacements = load_replacements(replace_file)

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(FILE_EXTENSIONS):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, replacements)

if __name__ == '__main__':
    process_files()
