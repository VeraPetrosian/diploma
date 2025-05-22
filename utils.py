import re
import os
import uuid
from pathlib import Path
import types
import subprocess
from manim import Scene, tempconfig  # Import Scene from manim
import openai
from typing import Optional
from config import OPENAI_API_KEY, MANIM_TEMPLATE
openai.api_key = OPENAI_API_KEY

class ProblemData:
    def __init__(self, problem_text: str, solution_text: str, theme: str, subtopic: str, difficulty: str):
        self.problem_text = problem_text
        self.solution_text = solution_text
        self.theme = theme
        self.subtopic = subtopic
        self.difficulty = difficulty

def generate_manim_prompt(solution_text: str) -> str:
    return f"""
Create a Python script for Manim (community version) that animates the following mathematical solution.
The animation should clearly visualize each step with appropriate mathematical notations and smooth transitions in  russian language and  with arithmetical figures if it's necessary.
 
Requirements:
1. The class must be named exactly 'SolutionScene' and inherit from 'Scene'
2. Use only basic Manim features (no LaTeX)
3. Keep the code simple and well-commented
4. Ensure the animation is self-explanatory
5. Use a clean, educational style with good pacing
6. All textes in animation should  be in russian
7. Add arithmetic figures if it's necessary
8. Add moderm and simple design
Primary requirements:
1. The animation must fully fit within the visible area of the video. It should not go beyond the video frame. If the solution is too long, just switch to a new line or allow scrolling (use only basic manim features.  no LaTeX)
2. Font size should be large enough to be easily readable and it should not go beyond the video frame, but not so large that it takes up too much space.    
Solution to animate:
{solution_text}
 
Return only the Python code with no additional explanation or markdown formatting.
The first line should be: 'from manim import *'
    """

def call_gpt4(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in creating educational animations with Manim."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"GPT API error: {str(e)}")

def render_manim_animation(
    code: str,
    scene_class: str = "SolutionScene",
    quality: str = "medium_quality",
    output_path: str = "videos"
) -> str:
    print(code)
    # First validate the code contains the required imports
    if "from manim import" not in code and "import manim" not in code:
        code = "from manim import *\n" + code
    
    mod = types.ModuleType("user_manim_scene")
    exec(code, mod.__dict__)
    
    # Try to find the scene class
    scene_cls = getattr(mod, scene_class)
   
    
    if scene_cls is None:
        available_classes = [name for name, obj in mod.__dict__.items() 
                           if isinstance(obj, type)]
        raise ValueError(
            f"No valid Scene subclass found. Available classes: {available_classes}\n"
            f"Generated code:\n{code}"
        )
    print(scene_cls)
    output_path = Path(output_path).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    with tempconfig({
        "quality": quality,
        "media_dir": str(output_path),
        "disable_caching": True,
        "preview": False,
    }):
        scene = scene_cls()
        scene.render()

        video_path = Path(scene.renderer.file_writer.movie_file_path)


    
        return f"videos/videos/720p30/{video_path.name}"

def extract_python_code(text: str) -> str:
    # First try to extract code between ```python ``` markers
    match = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Then try between ``` ```
    match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: return the whole text
    return text.strip()