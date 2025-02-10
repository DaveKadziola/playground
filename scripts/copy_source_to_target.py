# put py and ini in the same folder
# if not set execute command set BASE_PATH=<project-root-dir> | export PATH=<project-root-dir>
import os
import shutil

# Get BASE_PATH environment variable
# if not set execute command for example set BASE_PATH=E:\<project-root-dir>
BASE_PATH = os.getenv('BASE_PATH')
if not BASE_PATH:
    raise ValueError("BASE_PATH environment variable not set")

# config file path
CONFIG_PATH = os.path.join(BASE_PATH, 'copy_source_to_target.config')

# Verify config file exists
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file {CONFIG_PATH} not found")

# Global flag for overwrite all
overwrite_all = False

# file copy handling
with open(CONFIG_PATH, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = [p.strip() for p in line.split(';')]
        if len(parts) != 3:
            print(f"Skipping invalid line: {line}")
            continue

        source_rel, dest_rel, switch = parts

        if switch.lower() != 'y':
            continue

        source_path = os.path.join(BASE_PATH, source_rel)
        dest_path = os.path.join(BASE_PATH, dest_rel)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        try:
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
                print(f"Copied file: {source_rel} -> {dest_rel}")

            elif os.path.isdir(source_path):
                if os.path.exists(dest_path):
                    if overwrite_all:
                        shutil.rmtree(dest_path)
                        shutil.copytree(source_path, dest_path)
                        print(f"Auto-overwritten directory: {source_rel} -> {dest_rel}")
                    else:
                        response = input(f"Overwrite directory {dest_rel}? [y/n/a]: ").lower()
                        if response == 'a':
                            overwrite_all = True
                            shutil.rmtree(dest_path)
                            shutil.copytree(source_path, dest_path)
                            print(f"Overwritten directory (all): {source_rel} -> {dest_rel}")
                        elif response == 'y':
                            shutil.rmtree(dest_path)
                            shutil.copytree(source_path, dest_path)
                            print(f"Overwritten directory: {source_rel} -> {dest_rel}")
                        else:
                            print(f"Skipped directory: {dest_rel}")
                else:
                    shutil.copytree(source_path, dest_path)
                    print(f"Copied directory: {source_rel} -> {dest_rel}")

        except Exception as e:
            print(f"Error copying {source_rel}: {str(e)}")
