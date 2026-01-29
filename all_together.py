
import sys
import io
import gradio as gr

from secondary_functions import *

def project(file):
    text=file.name
    with open(text, 'r', encoding= 'utf-8') as f:
        result = f.read()
    
    result=check_patient(result)
    return result
   

interface = gr.Interface(
    fn=project,
    inputs=gr.File(label="upload a text file"),
    outputs=gr.Textbox(label="file analysis result")
)


interface.launch()
