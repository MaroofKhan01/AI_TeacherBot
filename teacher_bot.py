import os
import time
import json
from typing import Optional, Dict
from langdetect import detect, DetectorFactory
from dataclasses import dataclass
from prompts import TEACHER_STYLE_PROMPT

# Stable results for langdetect
DetectorFactory.seed = 42

# Optional: OpenAI backend (if key is present)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# Optional: Transformers fallback
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

SUPPORTED = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
}

DEFAULT_LOCAL_MODEL = "google/flan-t5-base"

@dataclass
class BotConfig:
    temperature: float = 0.3
    max_new_tokens: int = 512
    top_p: float = 0.9

class TeacherBot:
    def __init__(self, config: Optional[BotConfig] = None):
        self.config = config or BotConfig()
        self._init_backends()

    def _init_backends(self):
        self.use_openai = False
        self.client = None
        self.local_generator = None

        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key and OpenAI is not None:
            try:
                self.client = OpenAI()
                self.use_openai = True
            except Exception:
                self.client = None
                self.use_openai = False

        if not self.use_openai:
            # Load a small instruction-tuned model (Flan-T5)
            self.local_generator = pipeline(
                "text2text-generation",
                model=DEFAULT_LOCAL_MODEL,
                device_map="auto" if os.environ.get("USE_AUTO_DEVICE", "1") == "1" else None,
            )

    def detect_language(self, text: str) -> str:
        try:
            code = detect(text)
        except Exception:
            code = "en"
        # Map unknowns to nearest supported language
        return code if code in SUPPORTED else "en"

    def build_prompt(self, user_input: str, lang_code: str) -> str:
        lang_name = SUPPORTED.get(lang_code, "English")
        return f"Act as a knowledgeable teacher. Explain clearly in {lang_name} ({lang_code}) with examples. Question: {user_input.strip()}"

    def generate_openai(self, prompt: str) -> str:
        # Uses the latest text or chat completion API
        # Model names can be swapped; gpt-4o-mini is cost-effective
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        try:
            resp = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful teacher who responds with structured, educational answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_new_tokens,
                top_p=self.config.top_p,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"Error from OpenAI backend: {e}"

    def generate_local(self, prompt: str) -> str:
        out = self.local_generator(
            prompt,
            max_new_tokens=self.config.max_new_tokens,
            num_return_sequences=1
        )[0]["generated_text"]

        return out.strip()

    def answer(self, user_input: str) -> Dict:
        start = time.time()
        lang_code = self.detect_language(user_input)
        prompt = self.build_prompt(user_input, lang_code)

        if self.use_openai:
            output = self.generate_openai(prompt)
            backend = "openai"
        else:
            output = self.generate_local(prompt)
            backend = f"transformers:{DEFAULT_LOCAL_MODEL}"

        return {
            "language": {"code": lang_code, "name": SUPPORTED.get(lang_code, 'English')},
            "backend": backend,
            "prompt_used": prompt,
            "answer": output,
            "latency_sec": round(time.time() - start, 2),
        }

if __name__ == "__main__":
    bot = TeacherBot()
    print("TeacherBot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = bot.answer(user_input)
        print(f"\nBot ({response['language']['name']}): {response['answer']}\n")
