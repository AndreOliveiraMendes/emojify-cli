import os
import subprocess
import sys
import tempfile

def open_editor(filename=None, initial_message=''):
    """
    Opens the specified file in the user's default text editor and waits for it to close.
    If no filename is provided, a temporary file is used.
    """
    # Try to find the editor from environment variables
    editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
    
    # Define platform-specific fallbacks if environment variables are not set
    if not editor:
        if sys.platform.startswith("win"):
            # Use 'notepad.exe' on Windows as a common default
            editor = 'notepad.exe'
        elif sys.platform == "darwin":
            # Use 'open' command on macOS to launch the default app
            editor = 'open'
        else:
            # Use 'vim' or 'nano' on Linux as common defaults
            editor = 'vim' # or 'nano'

    # If no filename is provided, use a temporary file
    if not filename:
        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False, mode='w+') as tf:
            tf.write(initial_message)
            tf_name = tf.name
        try:
            # Call the editor and wait for the user to finish editing
            if sys.platform == "darwin":
                 subprocess.call([editor, tf_name]) # macOS uses "open filename"
            else:
                 subprocess.call([editor, tf_name])
            
            # Read the edited content back from the temporary file
            with open(tf_name, 'r') as tf:
                edited_message = tf.read()
            return edited_message
        finally:
            os.remove(tf_name) # Clean up the temporary file
    else:
        # Open the specific file and wait for the editor to close
        try:
            subprocess.call([editor, filename])
        except FileNotFoundError:
            print(f"Error: Editor '{editor}' not found. Please set your EDITOR environment variable.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example Usage:

# 1. Open a temporary editor to get user input
# user_input = open_editor(initial_message="Type your message here and save/close the editor...")
# print(f"\nUser edited message:\n{user_input}")

# 2. Open an existing file in the default editor
# open_editor(filename="my_script.py")
