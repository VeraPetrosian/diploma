import os
import dotenv
dotenv.load_dotenv()
# Конфигурационные параметры
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = "your-aws-access-key"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"
S3_BUCKET_NAME = "your-s3-bucket-name"

# Шаблон для Manim
MANIM_TEMPLATE = """
from manim import *

class SolutionScene(Scene):
    def construct(self):
        # Здесь будет код анимации
        # Используй self.add(), self.play() и другие методы Manim
        # Раздели решение на логические шаги
        # Добавь формулы с помощью Tex()
        pass
"""