from wiktionaryparser import WiktionaryParser
from re import match
import boto3
import json

#searches for dictionary form in case of conjugated verbs or adjectives or plural nouns
def decideDictionaryForm(regex, text, referenceWord):
    matchitem = match(regex, text)
    if matchitem:   #if not None
        return matchitem.group(1)
    return referenceWord

def lambda_handler(event, context):
    word = event['word']
    parser = WiktionaryParser()
    try:
        result = parser.fetch(word, 'italian')
    except Exception:
        return {
            'statuscode': 500,
            'body': json.dumps('Couldn\'t get dictionary form ')
        }


    if result and len(word) > 1:
        dictionary_form = []
        for i in result:
            definition = i['definitions']
            if definition:
                partOfSpeech, text = definition[0]['partOfSpeech'], definition[0]['text']

                # get dictionary form of certain parts of speech
                if partOfSpeech == 'adjective':
                    dictionary_form.append(decideDictionaryForm(r".*\sof\s([a-z]+)\s*.*$", text[1], word))
                elif partOfSpeech == 'noun':
                    dictionary_form.append(decideDictionaryForm(r".*plural\sof\s([a-z]+)", text[1], word))
                elif partOfSpeech == 'verb':
                    if not match(r".*to\s[a-z]+\s*.*", text[1]):
                        dictionary_form.append(decideDictionaryForm(r".*\sof\s([a-z]+(are|ire|ere|rsi|rci|rne|rla|rle|rcela|rcisi|rsela|rsene))\s*.*$", text[1], word))
                    else:
                        dictionary_form.append(word)
                elif partOfSpeech in ('adverb', 'numeral', 'preposition'):
                    dictionary_form.append(word)

        if dictionary_form:
            dictionary_form = set(dictionary_form)
            print(f"{word}: {dictionary_form}")
            aws_lambda = boto3.client('lambda')
            for i in dictionary_form:
                pass
                #aws_lambda.invoke(FunctionName='translate_and_save_dictionary_form',
                #                      InvocationType='Event',
                #                      LogType='Tail',
                #                      Payload=bytes(json.dumps({"dictionary_form": i}).encode())
                #        )

    else:
        #could't find word a definition
        print(f'Couldn\'t find dictionary form {word}')
    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }