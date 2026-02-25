import sys
import io
import gradio as gr

from secondary_functions import *

# Set to True for terminal-only mode using LIS_result.txt;
# False to use the Gradio website with uploaded files.
PRINT_TO_TERMINAL = False


def project(file):
    """
    Gradio callback: only used when PRINT_TO_TERMINAL is False.
    Reads the uploaded file, runs the checks, and returns output to the website.
    """
    with open(file.name, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    parsed = scrape_lines(lines)
    t = test_type(parsed)

    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    try:
        if t == "P":
            check_patient(parsed, t)
        elif t == "Q":
            check_qc(parsed, t)
        elif t == "C":
            check_calibration(parsed, t)
        else:
            print("Unknown or invalid test type:", t)
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


def run_cli():
    """
    Terminal-only mode: read LIS_result.txt and print checks to the terminal.
    """
    with open("LIS_result.txt", "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    parsed = scrape_lines(lines)
    t = test_type(parsed)
    # Show test type in the terminal (P/Q/C or "error")
    print("Test type:", t)

    if t == "P":
        check_patient(parsed, t)
    elif t == "Q":
        check_qc(parsed, t)
    elif t == "C":
        check_calibration(parsed, t)
    else:
        print("Unknown or invalid test type:", t)


if __name__ == "__main__":
    if PRINT_TO_TERMINAL:
        # No website at all, just run on LIS_result.txt and exit.
        run_cli()
    else:
        interface = gr.Interface(
            fn=project,
            inputs=gr.File(label="Upload an ASTM result file"),
            outputs=gr.Textbox(label="File Analysis")
        )
        # share=True creates a temporary public link you can share
        interface.launch(share=True)
