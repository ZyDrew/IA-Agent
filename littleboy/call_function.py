from google.genai import types
from functions.config import WORKING_DIR
from functions.get_files_info import schema_get_files_info, schema_get_file_content, get_file_content, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_call_part.args["working_directory"] = WORKING_DIR

    match function_call_part.name:
        case "get_files_info":
            result = get_files_info(**function_call_part.args)
        case "get_file_content":
            result = get_file_content(**function_call_part.args)
        case "run_python_file":
            result = run_python_file(**function_call_part.args)
        case "write_file":
            result = write_file(**function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )
    