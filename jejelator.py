import re
import random
import json


with open("normal_to_jejemon_variants.json", "r", encoding="utf-8") as f:
    normalization_dict = json.load(f)


leet_replacements = {
    'a': '4', 'e': '3', 'i': '1', 'o': '0', 'u': 'u',
    's': '5', 't': '7', 'b': '8', 'g': '9', 'l': '1'
}

reverse_leet = {
    '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's',
    '7': 't', '@': 'a', '$': 's', '+': 't', '8': 'b'
}


def normalize_leetspeak(word):
    return ''.join(reverse_leet.get(c.lower(), c.lower()) for c in word)


def to_jejemon(word):
    return ''.join(leet_replacements.get(c.lower(), c) for c in word)


def build_maps(data):
    translation_map = {}
    for category, words in data.items():
        for k, v in words.items():
            translation_map[k.lower()] = v
    return translation_map

translation_map = build_maps(normalization_dict)


def translate_sentence(user_input):
    def replacer(match):
        word = match.group(0)
        key = word.lower()
        normalized = normalize_leetspeak(key)

        if key in translation_map:
            return translation_map[key]
        elif normalized in translation_map:
            return translation_map[normalized]
        else:
            return to_jejemon(word)

    pattern = re.compile(r"\b[\w@#'!&.%-]+\b")
    return pattern.sub(replacer, user_input)


def chatbot_simulate():
    print("🤖 Jejelator is ready! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("👋 Bye!!")
            break

        translated = translate_sentence(user_input)
        print(f"\n📝 Translation:\n  {translated}\n")


if __name__ == "__main__":
    chatbot_simulate()
