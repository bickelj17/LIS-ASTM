#pip install --upgrade gradio
import gradio as gr
import os
 
def analyze_result(file):
    text=file.name
    
    with open(text, 'r', encoding= 'utf-8') as f:
        content = f.read()
    word_count= len(content.split())
    return f"The uploaded file contains {word_count} words."
    

interface = gr.Interface(
    fn=analyze_result,
    inputs=gr.File(label="upload a text file"),
    outputs=gr.Textbox(label="word count result")
)


interface.launch()