from pathlib import Path
from google.genai import types

def get_file_content(working_directory, file_path):
    working_path = Path(working_directory)
    if not working_path.exists():
        return f'Error: Working directory "{working_directory}" does not exist'
    full_file_path = working_path / file_path

    if working_path != full_file_path and working_path.absolute() not in full_file_path.resolve().parents:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not full_file_path.exists() or not full_file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with full_file_path.open('r', encoding='utf-8') as file:
            content = file.read(MAX_CHARS)
        if file.closed:  # Check if there is more content after reading MAX_CHARS
            content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: Error reading file "{file_path}": {str(e)}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)