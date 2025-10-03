import os
import subprocess
from functions.config import MAX_CHARS

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            base_args = ["python", abs_full_path]
            args = base_args + args
            completed_process = subprocess.run(args, capture_output=True, timeout=30, cwd=os.path.abspath(working_directory), text=True)

            if completed_process.returncode != 0:
                return f"Process exited with code {completed_process.returncode}"
            if completed_process.stdout == 0:
                return "No output produced"
            
            return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"

        except Exception as e:
            return f"Error: executing Python file: {e}"
        
        
    except Exception as e:
        return f"Error: {e}"