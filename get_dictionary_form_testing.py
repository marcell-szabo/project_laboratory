from wiktionaryparser import WiktionaryParser
from re import match

#searches for dictionary form in case of conjugated verbs or adjectives or plural nouns
def decideDictionaryForm(regex, text, referenceWord):
    matchitem = match(regex, text)
    if matchitem:   #if not None
        return matchitem.group(1)
    return referenceWord

def lambda_handler(event, context):
    word = event['word']
    parser = WiktionaryParser()
    result = parser.fetch(word, 'italian')
    if result and len(word) > 1:
        dictionary_form = []
        for i in result:
            definition = i['definitions']
            if definition:
                partofspeech, text = definition[0]['partOfSpeech'], definition[0]['text']
                #print(f"{definition[0]['partOfSpeech']} ---------------------------------{definition[0]['text']}")
                # get dictionary form of certain parts of speech
                if partofspeech == 'adjective':
                    dictionary_form.append(decideDictionaryForm(r".*\sof\s([a-z]+)\s*.*$", text[1], word))
                elif partofspeech == 'noun':
                    dictionary_form.append(decideDictionaryForm(r".*plural\sof\s([a-z]+)", text[1], word))
                elif partofspeech == 'verb':
                    if not match(r".*to\s[a-z]+\s*.*", text[1]):
                        dictionary_form.append(decideDictionaryForm(r".*\sof\s([a-z]+(are|ire|ere|rsi|rci|rne|rla|rle|rcela|rcisi|rsela|rsene))\s*.*$", text[1], word))
                    else:
                        dictionary_form.append(word)
                elif partofspeech in ('adverb', 'numeral', 'preposition'):
                    dictionary_form.append(word)

        dictionary_form = set(dictionary_form)
        print(f"#############################\n{dictionary_form}\n //////////////////////////////// \n")

    else:
        #could't find word a definition
        pass

if __name__ == '__main__':
    word = input()
    lambda_handler({"word": word}, None)