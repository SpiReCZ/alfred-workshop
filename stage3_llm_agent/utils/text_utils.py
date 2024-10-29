
import re
import Levenshtein
from typing import Tuple

LEVENSHTEIN_SCORE_CUTOFF = 0.70

def remove_preceding_text(text, actual_trigger_word):
    """Removes preceding text from the text if it is present. Case insensitive."""
    if re.search(f'(?i){re.escape(actual_trigger_word)}', text):
        return actual_trigger_word + '' + text.split(actual_trigger_word, 1)[-1]
    return text

def remove_trigger_word(text,actual_trigger_word):
    """Removes the trigger word from the text if it is present. Case insensitive."""
    text = re.sub(f'(?i){re.escape(actual_trigger_word)}', '', text)
    return text.strip()


def get_best_match(needle, text) -> Tuple[str, float]:
    """Returns the best match for the needle in the text and the ratio. 
    The best match is the longest substring of text that has the highest Levenshtein ratio to the needle"""
    # track best length and best ratio
    best_length = 1
    best_ratio = 0.0
    best_match = None


    # iterate over the full length of the text
    for j in range(len(text)):
        for i in range(j,len(text)):
            # compute Levhenstain ratio for the substring of length i and compare it to needle
            ratio = Levenshtein.ratio(needle.lower(), text[j:i].lower(), score_cutoff=LEVENSHTEIN_SCORE_CUTOFF)
            # if the ratio is better than the best ratio, update the best ratio and best length
            if ratio > best_ratio:
                best_ratio = ratio
                best_length = i
                best_ratio = ratio
                best_match = text[j:i]
    # return the best match and the best ratio
    # take up all following alphanumeric characters after best_match (whitespace breaks the word)
    if best_match is not None:
        for i in range(best_length, len(text)):
            if text[i].isalnum():
                best_match += text[i]
            else:
                break
    return best_match, best_ratio

def find_trigger_word(text, trigger_words_list) -> Tuple[str, str, float]:
    """Finds the trigger word in the text and returns it along with the best match in the form (trigger_word_key, best_match)"""
    #Iterate over key value pairs of TRIGGER_WORDS dictionary
    for trigger_word_key, trigger_words in trigger_words_list.items():
        # get best match for each trigger word
        for trigger_word in trigger_words:
            best_match, best_ratio = get_best_match(trigger_word, text)
            # if the best ratio is greater than 0.8, return the trigger word
            if best_ratio > (LEVENSHTEIN_SCORE_CUTOFF+0.1):
                print(f"Matching {trigger_word} against {best_match} -> similarity: {best_ratio}")
                return (trigger_word_key, best_match, best_ratio)
    return (None, None, None)
