import json
from pyonmttok import Tokenizer
from . import transliterate
import re
import os
from Levenshtein import distance

def load_dakshina_map():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dakshina_lexicon.json')) as f:
        return json.load(f)

def count_bangla_chars(line):
    chars = re.findall(r'[\u0981-\u0983\u0985-\u098B\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC\u09BE-\u09C3\u09C7-\u09C8\u09CB-\u09CC\u09CE\u09D7\u09DC-\u09DD\u09DF\u09E6-\u09EF\u09F3\u0964\u09F7]', line, flags=re.UNICODE)
    return len(chars)

class Transliterator:
    def __init__(self):
        self.word_map = load_dakshina_map()
        self.tokenizer = Tokenizer('aggressive')
        
    def process_line(self, line):
        processed_words = []
        
        line = line.strip()
        for word in line.split():
            processed_tokens = []

            for token in self.tokenizer.tokenize(word)[0]:
                if count_bangla_chars(token):
                    current_transliteration = transliterate.process('Bengali',
                                                                    'Custom',
                                                                    token,
                                                                    pre_options=['AnuChandraEqDeva', 'RemoveSchwaHindi', 'SchwaFinalBengali'],
                                                                    post_options=['RemoveDiacritics'])
                    transliteration_map = self.word_map.get(token, {})
                    if transliteration_map:
                        if current_transliteration in transliteration_map:
                            processed_tokens.append(current_transliteration)
                        else:
                            selected_transliteration = min([candidate for candidate in transliteration_map], 
                                                            key=lambda k: distance(current_transliteration, k))
                            processed_tokens.append(selected_transliteration)
                    else:
                        processed_tokens.append(current_transliteration)
                else:
                    processed_tokens.append(token)

            processed_words.append(''.join(processed_tokens))

        return ' '.join(processed_words)


