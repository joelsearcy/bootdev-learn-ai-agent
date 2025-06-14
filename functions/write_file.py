from pathlib import Path

def write_file(working_directory, file_path, content):
    working_path = Path(working_directory)
    if not working_path.exists():
        return f'Error: Working directory "{working_directory}" does not exist'
    full_file_path = working_path / file_path

    if working_path != full_file_path and working_path.absolute() not in full_file_path.resolve().parents:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not full_file_path.exists():
        # create the file and any necessary parent directories
        try:
            full_file_path.parent.mkdir(parents=True, exist_ok=True)
            full_file_path.touch()
        except Exception as e:
            return f'Error: Could not create file "{file_path}": {str(e)}'
    with full_file_path.open('w', encoding='utf-8') as file:
        try:
            file.write(content)
        except Exception as e:
            return f'Error: Could not write to file "{file_path}": {str(e)}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'