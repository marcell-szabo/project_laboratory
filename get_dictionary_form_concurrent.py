from wiktionaryparser import WiktionaryParser
from re import match
import boto3
import json
import concurrent.futures


def concurrent_lambdacall(dictionary_form, aws_lambda):
    try:
        aws_lambda.invoke(FunctionName='translate_and_save_dictionary_form',
                        InvocationType='Event',
                        LogType='Tail',
                        Payload=bytes(json.dumps({"dictionary_form": dictionary_form}).encode())
                      )
        print('invoked concurrent ')
    except Exception:
        print('Cannot invoke lambda')


# searches for dictionary form in text based on regex
def decideDictionaryForm(regex, text, referenceWord):
    matchitem = match(regex, text)
    if matchitem:  # if not None
        return matchitem.group(1)
    return referenceWord

def findDictionaryFormInResult(result, word):
    definition = result['definitions']
    if definition:
        partOfSpeech, text = definition[0]['partOfSpeech'], definition[0]['text']

        # get dictionary form of certain parts of speech (adjective, noun, verb, adverb, numeral, preposition)
        if partOfSpeech == 'adjective':
            return decideDictionaryForm(r".*\sof\s([a-z]+)\s*.*$", text[1], word)
        elif partOfSpeech == 'noun':
           return decideDictionaryForm(r".*plural\sof\s([a-z]+)", text[1], word)
        elif partOfSpeech == 'verb':
            if not match(r".*to\s[a-z]+\s*.*", text[1]):
                return decideDictionaryForm(
                    r".*\sof\s([a-z]+(are|ire|ere|rsi|rci|rne|rla|rle|rcela|rcisi|rsela|rsene))\s*.*$", text[1],
                    word)
            else:
                return word
        elif partOfSpeech in ('adverb', 'numeral', 'preposition'):
            return word
        else:
            return None
    else:
        return None


def lambda_handler(event, context):
    word = event['word']
    parser = WiktionaryParser()

    # parses italian Wiktionaryfor word
    try:
        result = parser.fetch(word, 'italian')
    except Exception:
        return {
            'statuscode': 500,
            'body': json.dumps('Couldn\'t get dictionary form ')
        }

    if result and len(word) > 1:
        # on average this is one iteration so it is not worth transforming it to concurrent
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = list(executor.map(lambda x: findDictionaryFormInResult(x, word), result))
            #futures = [executor.submit(findDictionaryFormInResult, i, word) for i in result]
        if any(future):
            dictionary_form = set(future)
            print(f"{word}: {dictionary_form}")
            aws_lambda = boto3.client('lambda')
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(lambda x: concurrent_lambdacall(x, aws_lambda), dictionary_form)
    else:
        # could't find word a definition
        print(f'Couldn\'t find dictionary form {word}')

    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }

if __name__ == '__main__':
    word = input()
    lambda_handler({"word": word}, None)