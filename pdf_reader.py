print("=== Document Question Assistant ===")

filename = "document.txt"

try:
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    print("Document loaded successfully!")

    question = input("Enter a keyword to search: ").lower()

    sentences = text.replace("?", ".").split(".")

    results = [
        sentence.strip()
        for sentence in sentences
        if question in sentence.lower()
    ]

    if results:
        print("\nMatching information:")
        for result in results:
            print("-", result)
    else:
        print("No matching information found.")

except FileNotFoundError:
    print("Please create document.txt first.")
