import re
import random
import json


with open("normal_to_jejemon_variants.json", "r", encoding="utf-8") as f:
    normalization_dict = json.load(f)


leet_replacements = {
    '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's',
    '7': 't', '@': 'a', '$': 's', '+': 't', '8': 'b'
}


def normalize_leetspeak(word):
    return ''.join(leet_replacements.get(char.lower(), char.lower()) for char in word)


def build_maps(data):
    translation_map = {}
    word_response_map = {}
    for category, words in data.items():
        for k, v in words.items():
            k_lower = k.lower()
            translation_map[k_lower] = v
            word_response_map[k_lower] = [f"'{k}' means '{v}'"]
    return translation_map, word_response_map


translation_map, word_response_map = build_maps(normalization_dict)


def process_input(user_input):
    words = re.findall(r"\b[\w@#'!&.%-]+\b", user_input)
    results = {}
    for word in words:
        key = word.lower()
        normalized = normalize_leetspeak(key)
        if key in translation_map:
            results[word] = {
                "meaning": translation_map[key],
                "response": random.choice(word_response_map[key])
            }
        elif normalized in translation_map:
            results[word] = {
                "meaning": translation_map[normalized],
                "response": f"'{word}' (normalized from leetspeak) means '{translation_map[normalized]}'"
            }
    return results


def translate_sentence(user_input):
    def replacer(match):
        word = match.group(0)
        key = word.lower()
        normalized = normalize_leetspeak(key)
        if key in translation_map:
            return translation_map[key]
        elif normalized in translation_map:
            return translation_map[normalized]
        return word

    pattern = re.compile(r"\b[\w@#'!&.%-]+\b")
    return pattern.sub(replacer, user_input)


def chatbot_simulate():
    print("🤖 Jejelator is ready! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("👋 Bye!!")
            break

        matches = process_input(user_input)
        translated = translate_sentence(user_input)

        if matches:
            print(f"\n📝 Translation:\n  {translated}\n")
        else:
            print("🤷 Sorry, no jejemon words found.\n")


if __name__ == "__main__":
    chatbot_simulate()
