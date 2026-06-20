import re
import ftfy
import unicodedata

def normalize_unicode(text):

    if not isinstance(text,str):
        return text

    # Fix encoding issues
    text = ftfy.fix_text(text)

    # Unicode Normalization
    text = unicodedata.normalize("NKFC",text)

    # Remove invisible characters
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')

    return text
