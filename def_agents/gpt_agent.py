import os
from openai import OpenAI
import json

# OpenAI クライアントの初期化
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class DebateJudgeAgent:
    def __init__(self, name: str, model: str, max_tokens: int, temperature: float, prompt_path: str):
        self.name = name
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.memory = []
        self.load_prompt(prompt_path)

    def load_prompt(self, prompt_path):
        with open(prompt_path, 'r') as file:
            prompts = json.load(file)
            self.system_prompt = prompts["system_prompt"]
            self.user_prompt = prompts["user_prompt"]
        self.set_system(self.system_prompt)

    def set_system(self, system_prompt):
        self.memory.append({"role": "system", "content": system_prompt})

    def add_user(self, user_message):
        self.memory.append({"role": "user", "content": user_message})

    def add_assistant(self, assistant_message):
        self.memory.append({"role": "assistant", "content": assistant_message})

    def evaluate(self, debate_text):
        user_message = self.user_prompt.replace("###debate_text###", debate_text)
        self.add_user(user_message)
        
        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=self.memory,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            evaluation = completion.choices[0].message.content
            self.add_assistant(evaluation)
            return evaluation
        except Exception as e:
            print(f"Error in API call: {e}")
            return None

def create_agents(criteria, model, max_tokens, temperature, prompt_paths):
    return {criterion: DebateJudgeAgent(criterion, model, max_tokens, temperature, prompt_paths[criterion]) 
            for criterion in criteria}