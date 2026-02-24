
import sys
import io
import gradio as gr

from secondary_functions import *


def project(file):
    """
    Gradio callback:
    - reads the uploaded file
    - parses it into ASTM fields
    - runs the existing patient checks
    - returns everything that would normally be printed to the console
    """
    # Capture all prints from the checking functions
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        with open(file.name, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        # Use existing helpers imported via secondary_functions -> base_functions
        parsed = scrape_lines(lines)
        check_patient(parsed)
    finally:
        # Restore normal stdout even if something goes wrong
        sys.stdout = old_stdout

    # Send the captured log back to the Gradio textbox
    return buffer.getvalue()
   

interface = gr.Interface(
    fn=project,
    inputs=gr.File(label="upload a text file"),
    outputs=gr.Textbox(label="file analysis result")
)


interface.launch()
