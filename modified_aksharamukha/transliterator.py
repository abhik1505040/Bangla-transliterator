import json
from pyonmttok import Tokenizer
from . import transliterate
import re
import os
from Levenshtein import distance

BANGLA_CHARS = re.compile(r'[\u0981-\u0983\u0985-\u098B\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC\u09BE-\u09C3\u09C7-\u09C8\u09CB-\u09CC\u09CE\u09D7\u09DC-\u09DD\u09DF\u09E6-\u09EF\u09F3\u0964\u09F7]', 
                          flags=re.UNICODE)

def load_dakshina_map():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dakshina_lexicon.json')) as f:
        return json.load(f)

class Transliterator:
    def __init__(self):
        self.word_map = load_dakshina_map()
        self.tokenizer = Tokenizer('aggressive')
        
    def process_line(self, line, rule_based_only=False):
        processed_words = []
        
        line = line.strip()
        for word in line.split():
            processed_tokens = []

            for token in self.tokenizer.tokenize(word)[0]:
                if BANGLA_CHARS.search(token):
                    current_transliteration = transliterate.process('Bengali',
                                                                    'Custom',
                                                                    token,
                                                                    pre_options=['AnuChandraEqDeva', 'RemoveSchwaHindi', 'SchwaFinalBengali'],
                                                                    post_options=['RemoveDiacritics'])

                    if not rule_based_only:
                        transliteration_map = self.word_map.get(token, {})
                        if transliteration_map:
                            # approach 1: use only edit distance
                            # selected_transliteration = min(transliteration_map, key=lambda k: distance(current_transliteration, k))

                            # approach 2: use attestation scores with edit distance as tiebreaker
                            highest_scored_transliteration = max(transliteration_map, 
                                                                    key=lambda k: int(transliteration_map[k]))
                            highest_score = transliteration_map[highest_scored_transliteration]
                            candidate_transliterations = [k for k, v in transliteration_map.items() if v == highest_score]

                            if len(candidate_transliterations) > 1:
                                selected_transliteration = min(candidate_transliterations, 
                                                                key=lambda k: distance(current_transliteration, k))
                            else:
                                selected_transliteration = highest_scored_transliteration

                            processed_tokens.append(selected_transliteration)
                            
                        else:
                            processed_tokens.append(current_transliteration)
                    else:
                        processed_tokens.append(current_transliteration)

                else:
                    processed_tokens.append(token)

            processed_words.append(''.join(processed_tokens))

        return ' '.join(processed_words)


