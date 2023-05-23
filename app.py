from flask import Flask, render_template, request, jsonify
from happytransformer import HappyTextToText, TTSettings
from spellchecker import SpellChecker

app = Flask(__name__)

# Initialize the HappyTextToText model
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Initialize the SpellChecker
spell = SpellChecker(language="en")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    input_text = request.json["input_text"]

    # Perform spelling correction
    words = input_text.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_text = " ".join(corrected_words)

    # Perform grammar correction
    result = happy_tt.generate_text(corrected_text, args=args)
    corrected_text = result.text

    return jsonify(corrected_text=corrected_text)

if __name__ == "__main__":
    app.run()

#http://127.0.0.1:5000/