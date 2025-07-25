import re
import json
import difflib


with open('jejemon_to_normal_variants.json', 'r', encoding='utf-8') as f:
    translation_map = json.load(f)


known_words = list(set(translation_map.values()))


leet_replacements = {
    '0': 'o', '1': 'i', '3': 'e', '4': 'a',
    '5': 's', '7': 't', '@': 'a', '$': 's',
    '+': 't', '8': 'b'
}

def smart_normalize(word):
    word = word.lower()
    word = re.sub(r"[^a-z0-9]", "", word)
    return ''.join(leet_replacements.get(c, c) for c in word)

def closest_mainword(word):
    normalized = smart_normalize(word)
    match = difflib.get_close_matches(normalized, known_words, n=1, cutoff=0.6)
    return match[0] if match else word

def translate_jejemon_to_normal(text):
    words = re.findall(r'\b[\w@#\'!&.%-]+\b', text)
    translated_words = []

    for word in words:
        key = word.lower()
        if key in translation_map:
            translated_words.append(translation_map[key])
        else:
            translated_words.append(closest_mainword(key))

    return ' '.join(translated_words)

def chatbot_simulate():
    print("👾 Jejelator (Jejemon ➡ Normal) is ready!\nType 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("👋 Bye!")
            break

        translated = translate_jejemon_to_normal(user_input)
        print(f"📝 Translation:\n{translated}\n")

if __name__ == "__main__":
    chatbot_simulate()
