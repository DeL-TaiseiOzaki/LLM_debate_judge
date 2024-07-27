import json

def load_prompt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt_data = json.load(file)
    return prompt_data["prompt"]