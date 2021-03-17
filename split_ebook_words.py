import json
import re
import boto3

def lambda_handler(event, context):
    paragraph = re.sub(r"/n/", r"\n", event['paragraph'])
    words = re.split(r"\s", paragraph)
    words = list(map(lambda x: re.sub(r'.*[./,:";()—!?-]+.*', "", x), words))
    words = list(filter(lambda x: re.fullmatch(r"[a-zA-Z]+", x), words))
    words = list(map(lambda x: x.lower(), words))
    dict_of_words = {}
    for i in words:
        if i in dict_of_words:
            dict_of_words[i] += 1
        else:
            dict_of_words[i] = 1

    aws_lambda = boto3.client('lambda')
    for i in dict_of_words.keys():
        aws_lambda.invoke(FunctionName='get_dictionary_form',
                          InvocationType='Event',
                          LogType='Tail',
                          Payload=bytes(json.dumps({"word": i}).encode())
        )

    return {
        "statuscode": 200,
        "body": json.dumps("OK")
    }