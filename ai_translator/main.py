import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslator, TranslationConfig

if __name__ == "__main__":
    # Parse command line arguments
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # Initialize configuration singleton
    config = TranslationConfig()
    config.initialize(args)    

    # Instantiate PDFTranslator class and call translate_pdf() method
    translator = PDFTranslator(config.model_name)
    translator.translate_pdf(config.input_file, config.output_file_format, pages=None)
