from flask import Flask, jsonify, render_template, send_from_directory, request
import os
import subprocess
import logging

app = Flask(__name__)

def load_text_from_file():
    file_path = os.path.join(os.path.dirname(__file__), 'english_chapter.txt')
    with open(file_path, 'r') as f:
        return f.read()

@app.route('/start-server', methods=['POST'])
def start_server():
    # Logic to start your Flask server
    # This could be a subprocess call to another Flask application
    try:
        # Example: Start a subprocess for the new server
        subprocess.Popen(['python', '/Users/ankityadav/Desktop/Hackathon/second copy 4/backend/app.py.py'])  # Adjust with your script name
        return jsonify({"message": "Flask server started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login-signup.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student-dashboard.html')

@app.route('/teacher-dashboard')
def teacher_dashboard():
    return render_template('teacher-dashboard.html')

@app.route('/download-notes')
def download_notes():
    course_note = request.args.get('course')
    return send_from_directory(os.path.dirname(__file__), course_note, as_attachment=True)



@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    try:
        if 'file' not in request.files:
            app.logger.error("No file part in request")
            return jsonify({"error": "No file uploaded"}), 400
        
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            app.logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400
        
        app.logger.info(f"Received file: {uploaded_file.filename}")
        chapter_text = uploaded_file.read().decode('utf-8')
        app.logger.info(f"File content length: {len(chapter_text)} characters")

        command = ["ollama", "run", "llama3.1"]
        result = subprocess.run(command, input=chapter_text, capture_output=True, text=True)
        
        app.logger.info("Ollama output: %s", result.stdout.strip())
        app.logger.error("Ollama error: %s", result.stderr)

        if result.returncode == 0:
            questions = result.stdout.strip().split('\n\n')
            app.logger.info("Generated questions: %s", questions)
            return jsonify({"output": questions})
        else:
            app.logger.error("Failed to generate questions: %s", result.stderr)
            return jsonify({"error": "Failed to generate questions", "details": result.stderr}), 500
    except Exception as e:
        app.logger.exception("Exception occurred")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=7000 )
