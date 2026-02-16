import os
import tempfile
import subprocess

def open_editor_with_content(initial_content: str) -> str: 
    """
    Opens vi with the given initial content. 

    Args:
        initial_content (str): The content to pre-populate in the editor.

    Returns:    
        str: The content after editing.
    """

    # Create a temporary file 
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(initial_content.encode())
        tmp_file.flush()

    try: 
        # open the editor
        subprocess.call(["vi", tmp_file_path])

        # Read the edited content
        with open(tmp_file_path, "r") as f:
            edited_content = f.read()

        return edited_content.strip()
    
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)