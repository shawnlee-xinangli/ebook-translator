import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, send_file, jsonify
from translator import PDFTranslator, TranslationConfig
from utils import ArgumentParser, LOG

app = Flask(__name__)

TEMP_FILE_DIR = "flask_temps/"

@app.route('/translation', methods=['POST'])
def translation():
    try:
        input_file = request.files['input_file']
        source_language = request.form.get('source_language', 'English')
        target_language = request.form.get('target_language', 'Chinese')

        LOG.debug(f"[input_file]\n{input_file}")
        LOG.debug(f"[input_file.filename]\n{input_file.filename}")

        if input_file and input_file.filename:
            # Create temporary file
            input_file_path = TEMP_FILE_DIR+input_file.filename
            LOG.debug(f"[input_file_path]\n{input_file_path}")

            input_file.save(input_file_path)

            # Call translation function
            output_file_path = Translator.translate_pdf(
                input_file=input_file_path,
                source_language=source_language,
                target_language=target_language)
            
            # Remove temporary file
            # os.remove(input_file_path)

            # Construct complete file path
            output_file_path = os.getcwd() + "/" + output_file_path
            LOG.debug(output_file_path)

            # Return translated file
            return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response), 400


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
    # Launch Flask Web Server
    app.run(host="0.0.0.0", port=5000, debug=True)