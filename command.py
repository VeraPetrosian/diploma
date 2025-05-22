import requests

url = 'http://localhost:5001/api/generate' # My API

data = {
    "problem_text": """Найдите наименьшее значение выражения (x² - 4x + 5) / (x² + 4x + 5) при x ∈ R.""",
    "solution_text": """Рассмотрим числитель и знаменатель по отдельности:
                        Числитель: x² - 4x + 5 = (x - 2)² + 1
                        Знаменатель: x² + 4x + 5 = (x + 2)² + 1
                        Тогда выражение принимает вид: f(x) = ((x - 2)² + 1) / ((x + 2)² + 1)
                        Это дробь, где числитель и знаменатель всегда положительные, значит функция всегда положительна.
                        Подставим некоторые значения x, чтобы найти наименьшее значение:
                        x = 0 ⇒ f(0) = (0 - 2)² + 1 / (0 + 2)² + 1 = (4 + 1) / (4 + 1) = 5 / 5 = 1
                        x = 2 ⇒ f(2) = (2 - 2)² + 1 / (2 + 2)² + 1 = (0 + 1) / (16 + 1) = 1 / 17 ≈ 0.0588
                        x = 3 ⇒ f(3) = (1 + 1) / (25 + 1) = 2 / 26 = 1 / 13 ≈ 0.0769
                        Наименьшее значение достигается при x = 2 и равно 1 / 17.""",
    "theme": "Math",
    "subtopic": "Arithmetic",
    "difficulty": "Easy"
}

# Make the POST request and get the streaming response
response = requests.get(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    with open('output.mp4', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Video saved as output.mp4")
else:
    print("Failed to generate video:", response.status_code, response.text)
