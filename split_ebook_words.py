import json
import re
import boto3
import concurrent.futures


def concurrent_lambdacall(word, aws_lambda):
    try:
        aws_lambda.invoke(FunctionName='get_dictionary_form',
                          InvocationType='Event',
                          LogType='Tail',
                          Payload=bytes(json.dumps({"word": word}).encode()))
        print('invoked concurrent 20')
    except Exception:
        print(f'aws exception for {word}')


def lambda_handler(event, context):
    paragraph = re.sub(r"/n/", r"\n", event['paragraph'])
    words = re.split(r"\s", paragraph)

    # keeping words
    words = list(map(lambda x: re.sub(r'.*[./,:";()—!?-]+.*', "", x), words))  # eliminate punctuation marks
    words = list(filter(lambda x: re.fullmatch(r"[a-zA-Z\u00C0-\u017F]+", x), words))
    words = list(map(lambda x: x.lower(), words))

    # keeping only unique words
    dict_of_words = {}
    for i in words:
        if len(i) > 1:
            if i in dict_of_words:
                dict_of_words[i] += 1
            else:
                dict_of_words[i] = 1
    aws_lambda = boto3.client('lambda')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: concurrent_lambdacall(x, aws_lambda), list(dict_of_words.keys()))
    return {
        "statuscode": 200,
        "body": 'Everything is OK'
    }