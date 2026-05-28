# scripts/normalize.py
import re
import sys

def convert_punctuation(text):
    mapping = {
        '，': ', ', '。': '. ', '：': ': ', '；': '; ',
        '！': '! ', '？': '? ', '（': ' (', '）': ') ',
        '、': ', '
    }

    pattern = r'(```[\s\S]*?```|`.*?`|\$\$[\s\S]*?\$\$|\$.*?\$)'
    parts = re.split(pattern, text)
    new_parts = []

    punct_re = re.compile('|'.join(re.escape(k) for k in mapping.keys()))

    for part in parts:
        if part.startswith(('```', '`', '$')):
            new_parts.append(part)
        else:
            res = punct_re.sub(lambda x: mapping[x.group()], part)
            res = re.sub(r' +', ' ', res)
            new_parts.append(res)

    return "".join(new_parts)

if __name__ == "__main__":
    input_text = sys.stdin.read()
    sys.stdout.write(convert_punctuation(input_text))
