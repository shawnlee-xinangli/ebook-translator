import sys
import os
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslator, TranslationConfig


def translation(input_file, source_language, target_language):
    LOG.debug(f"[Translation Task]\nSource file: {input_file.name}\nSource language: {source_language}\nTarget language: {target_language}")

    output_file_path = Translator.translate_pdf(
        input_file.name, source_language=source_language, target_language=target_language)

    return output_file_path

def launch_gradio():

    iface = gr.Interface(
        fn=translation,
        title="PDF e-Book Translator",
        inputs=[
            gr.File(label="Upload PDF file"),
            gr.Textbox(label="Source Language (Default: English)", placeholder="English", value="English"),
            gr.Textbox(label="Target Language (Default: Simplified Chinese)", placeholder="Simplified Chinese", value="Chinese")
        ],
        outputs=[
            gr.File(label="Download translated file")
        ],
        allow_flagging="never"
    )

    iface.launch(share=True, server_name="0.0.0.0")

def initialize_translator():
    # Parse command line arguments
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # Initialize configuration singleton
    config = TranslationConfig()
    config.initialize(args)    
    # Instantiate PDFTranslator class and call translate_pdf() method
    global Translator
    Translator = PDFTranslator(config.model_name)


if __name__ == "__main__":
    # Initialize translator
    initialize_translator()
    # Launch Gradio service
    launch_gradio()
