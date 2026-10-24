
import re
from datetime import datetime

FILENAME = "document.txt"
OUTPUT_FILE = "answer_history.txt"

STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "how",
    "why", "when", "where", "in", "of", "to",
    "and", "for", "does", "do", "explain", "tell", "me"
}

def tokenize(text):
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))

def find_answers(text, question):
    keywords = tokenize(question) - STOP_WORDS
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    results = []

    for sentence in sentences:
        words = tokenize(sentence)
        matched = keywords & words

        if matched:
            score = len(matched) / max(len(keywords), 1)
            results.append((score, sentence.strip()))

    results.sort(key=lambda item: item[0], reverse=True)
    return results[:5]

try:
    with open(FILENAME, "r", encoding="utf-8") as file:
        document = file.read()

    if not document.strip():
        raise ValueError("The document is empty.")

    print("===== DOCUMENT ASSISTANT =====")
    print("Document loaded. Type 'bye' to exit.")

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() == "bye":
            print("Assistant: Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        answers = find_answers(document, question)

        if answers:
            print("\nRelevant sentences:")
            for score, sentence in answers:
                print(f"- {sentence} (match: {score:.0%})")
        else:
            print("No matching information found.")

        with open(OUTPUT_FILE, "a", encoding="utf-8") as history:
            history.write(
                f"\n[{datetime.now().isoformat(timespec='seconds')}] "
                f"Question: {question}\n"
            )

            if answers:
                for score, sentence in answers:
                    history.write(f"Answer: {sentence}\n")
            else:
                history.write("Answer: No matching information found.\n")

except FileNotFoundError:
    print("Error: Create document.txt in the same folder.")
except ValueError as error:
    print("Error:", error)
except OSError as error:
    print("File error:", error)
