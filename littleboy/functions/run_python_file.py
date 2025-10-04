import os
import subprocess
from functions.config import MAX_CHARS
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            base_args = ["python", abs_full_path]
            args = base_args + args
            completed_process = subprocess.run(args, capture_output=True, timeout=30, cwd=abs_working_dir, text=True)

            if completed_process.returncode != 0:
                return f"Process exited with code {completed_process.returncode}"
            if completed_process.stdout:
                return "No output produced"
            
            return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"

        except Exception as e:
            return f"Error: executing Python file: {e}"
        
        
    except Exception as e:
        return f"Error: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)