from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Replace with your actual API key
GOOGLE_API_KEY = 'AIzaSyDVhQxYaYQ1wzL1c9i567TlQIIqFbMxVbY'

# Language code to name mapping (optional, for display)
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
}


def translate_text(text, source_lang, target_lang):
    url = "https://translation.googleapis.com/language/translate/v2"

    # Prepare parameters
    params = {
        "q": text,
        "target": target_lang,
        "format": "text",
        "key": GOOGLE_API_KEY
    }

    # Only add 'source' if it's NOT auto
    if source_lang != "auto":
        params["source"] = source_lang

    # Send request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["data"]["translations"][0]
        translated_text = data["translatedText"]
        detected_lang = data.get("detectedSourceLanguage", source_lang)
        return translated_text, detected_lang
    else:
        return f"Error: {response.status_code} - {response.text}", None



@app.route("/", methods=["GET", "POST"])
def home():
    translated = ""
    detected_lang = ""
    source_lang = ""
    target_lang = ""
    text = ""

    if request.method == "POST":
        text = request.form["text"]
        source_lang = request.form["source"]
        target_lang = request.form["target"]
        translated, detected_lang = translate_text(text, source_lang, target_lang)

    return render_template("index.html",
                           translated=translated,
                           detected_lang=detected_lang,
                           source_lang=source_lang,
                           target_lang=target_lang,
                           text=text,
                           LANGUAGES=LANGUAGES)


if __name__ == "__main__":
    app.run(debug=True)
