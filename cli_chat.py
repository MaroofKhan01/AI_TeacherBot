from teacher_bot import TeacherBot
import sys

BANNER = """
==========================================
 TeacherBot (Multilingual, Teacher-Style)
 Type 'exit' to quit
==========================================
"""

def main():
    bot = TeacherBot()
    print(BANNER)
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if user.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user:
            continue
        resp = bot.answer(user)
        lang = resp["language"]["name"]
        backend = resp["backend"]
        print(f"\n[Language: {lang} | Backend: {backend}]")
        print("TeacherBot:", resp["answer"].strip(), "\n")

if __name__ == "__main__":
    main()
