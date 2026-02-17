from flask import Flask, request, jsonify, render_template
import random
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start')
def start():
    return render_template("start.html")

@app.route('/generate_from_text', methods=['POST'])
def generate_from_text():
    data = request.get_json()
    text = data.get("text", "")
    qtype = data.get("qtype", "MCQ")
    qcount = int(data.get("qcount", 3))
    mcqcount = int(data.get("mcqcount", 4))

    # Check if the text is valid
    if not text or len(text.split()) < 10:
        return jsonify({"status": "error", "message": "Text too short"})

    # Split the text into sentences and choose the ones that are long enough
    sentences = [s.strip() for s in text.split('.') if len(s.split()) > 6]
    selected = random.sample(sentences, min(qcount, len(sentences)))

    questions = []
    for sent in selected:
        words = sent.split()
        keyword = random.choice(words)  # Random word to replace with blank
        question = sent.replace(keyword, "_____")  # Replace the word with blank

        # Create options for MCQ
        options = random.sample(words, min(mcqcount - 1, len(words)))
        if keyword not in options:
            options.append(keyword)  # Ensure the answer is among the options

        options = list(set(options))  # Ensure unique options
        random.shuffle(options)  # Shuffle the options

        # Add the generated question to the list
        questions.append({
            "question": question,
            "options": options,
            "answer": keyword
        })

    return jsonify({"status": "success", "questions": questions})

if __name__ == '__main__':
    app.run(debug=True)
