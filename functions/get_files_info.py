from pathlib import Path
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_path = Path(working_directory)
    if not working_path.exists():
        return f'Error: Working directory "{working_directory}" does not exist'
    if directory is not None:
        # check if the directory exists in the working directory
        dir_path = Path(working_directory) / directory
        if working_path != dir_path and working_path.absolute() not in dir_path.resolve().parents:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not dir_path.exists() or not dir_path.is_dir():
            return f'Error: "{directory}" is not a directory'

        working_path = dir_path
    
    results = ""
    for file in working_path.iterdir():
        results += f"- {file.name}:, file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}\n"
        
    return results if results else f'No files found in directory "{dir_path}"'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)