import re

def remove_stop_words(content, sw_path):
    stop_words = [word.strip().lower() for word in open(sw_path, 'r').readlines()]
    stop_words = sorted(stop_words, key=len, reverse=True)
    result = content.lower()
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    result = result.translate(translator)
    for word in stop_words:
        if word.startswith("`"):
            result = result.replace(word.removeprefix("`"), " ")
        else:
            result = result.replace(f" {word} ", " ")
    result = re.sub(' +', ' ', result)
    return result