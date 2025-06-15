from pathlib import Path

def run_python_file(working_directory, file_path):
    working_path = Path(working_directory)
    if not working_path.exists():
        return f'Error: Working directory "{working_directory}" does not exist'
    full_file_path = working_path / file_path

    if working_path != full_file_path and working_path.absolute() not in full_file_path.resolve().parents:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not full_file_path.exists() or not full_file_path.is_file():
        return f'Error: File "{file_path}" not found.'
    if full_file_path.suffix != '.py':
        return f'Error: "{file_path}" is not a Python file.'
    try:
        import subprocess
        result = subprocess.run(['python3', file_path], capture_output=True, cwd=working_directory, text=True, timeout=30)
        output = ''
        if result.stdout or result.stderr:
            output = f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}\n'
        else:
            output = 'No output produced.\n'
        
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}'
        return output
    except Exception as e:
        return f'Error: executing Python file: {e}'