import os
from google.genai import types
from functions.config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
    
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot list {directory} as it is outside the permitted working directory"
        
        if os.path.isfile(directory):
            return f"Error: {directory} is not a directory"
        
        dir_contents = os.listdir(full_path)
        if directory == ".":
            result = "Result for current directory:\n"
        else:
            result = f"Result for '{directory}' directory:\n"

        for content in dir_contents:
            result += (f"- {content}: file_size={os.path.getsize(os.path.join(full_path, content))} bytes," 
            f" is_dir={os.path.isdir(os.path.join(full_path, content))}\n")
    
    except Exception as e:
        return f"Error: {e}"
    
    return result

def get_file_content(working_directory, file_path):
    try:
        abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_full_path.startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
        
        if not os.path.isfile(abs_full_path):
            return f"Error: File not found or is not a regular file: {file_path}"
        
        with open(abs_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if os.path.getsize(abs_full_path) > MAX_CHARS:
            file_content_string += f"\n[...File {file_path} truncated at 10000 characters]"

        return file_content_string

    except Exception as e:
        return f"Error: {e}"
    

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
