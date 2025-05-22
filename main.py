import os
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file
from utils import (
    generate_manim_prompt,
    call_gpt4,
    render_manim_animation,
    extract_python_code,
    ProblemData
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'videos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

@app.route('/api/generate', methods=['POST', 'GET'])
def generate_video():
        data = request.get_json()
        
        # Validate input
        if not all(key in data for key in ['problem_text', 'solution_text', 'theme', 'subtopic', 'difficulty']):
            return jsonify({'error': 'Missing required fields'}), 400

        problem_data = ProblemData(
            problem_text=data['problem_text'],
            solution_text=data['solution_text'],
            theme=data['theme'],
            subtopic=data['subtopic'],
            difficulty=data['difficulty']
        )

        # Generate Manim code
        prompt = generate_manim_prompt(problem_data.solution_text)
        gpt_response = call_gpt4(prompt)
        manim_code = extract_python_code(gpt_response)
        
        if not manim_code:
            return jsonify({'error': 'Failed to generate valid Manim code'}), 500

        # Render animation
        video_path = render_manim_animation(manim_code, output_path=app.config['UPLOAD_FOLDER'])
        print(f"video_path: {video_path}")
        return send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=False  # Set to True to force download
    )

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5001, debug=True)