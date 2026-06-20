import re

def whitespace_normalization(text):
    if not isinstance(text,str):
        return text

    # Replace all whitespaces with single space
    text = re.sub(r'\s+',' ',text)

    # Remove leading and trailing whitespaces
    text = text.strip()

    return text
