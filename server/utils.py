import re

def markdown_to_function(markdown_text, function_name="generated_function"):
    # Find code blocks in Markdown text
    code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', markdown_text, re.DOTALL)

    if not code_blocks:
        return None  # No code blocks found

    # Join code blocks into a single string
    python_code = '\n'.join(code_blocks)

    # Remove any Markdown formatting syntax
    python_code = re.sub(r'^(?:[*_-]|\d+\.)\s+', '', python_code, flags=re.MULTILINE)

    # Wrap the code in a function definition
    function_definition = f"def {function_name}():\n"
    indented_code = '\n'.join(f"    {line}" for line in python_code.split('\n'))
    python_function = function_definition + indented_code

    return python_function