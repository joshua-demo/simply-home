import re

def markdown_to_function(markdown_text:str):
    # Find code blocks in Markdown text
    code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', markdown_text, re.DOTALL)

    if not code_blocks:
        return None  # No code blocks found

    # Join code blocks into a single string
    python_code = '\n'.join(code_blocks)

    # Remove any Markdown formatting syntax
    python_code = re.sub(r'^(?:[*_-]|\d+\.)\s+', '', python_code, flags=re.MULTILINE)

    return python_code.strip() 