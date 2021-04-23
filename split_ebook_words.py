import json
import re
import boto3


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
        if i in dict_of_words:
            dict_of_words[i] += 1
        else:
            dict_of_words[i] = 1
    aws_lambda = boto3.client('lambda')
    for i in dict_of_words.keys():
        try:
            aws_lambda.invoke(FunctionName='get_dictionary_form',
                              InvocationType='Event',
                              LogType='Tail',
                              Payload=bytes(json.dumps({"word": i}).encode())
                              )
            print('invoked')
        except Exception as e:
            print(e)
            return {
                "statuscode": 500,
                "body": json.dumps("server error")
            }
    return {
        "statuscode": 200,
        "body": json.dumps(dict_of_words)
    }