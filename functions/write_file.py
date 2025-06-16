from pathlib import Path
from google.genai import types

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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If the file does not exist, it will be created along with any necessary parent directories.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If the file already exists, it will be overwritten.",
            ),
        },
    ),
)