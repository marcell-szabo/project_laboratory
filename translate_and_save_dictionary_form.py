import boto3
import json

def lambda_handler(event, context):
    TABLE_NAME = 'translated_ebook_words'
    BUCKET_NAME = 'pronounced-words'
    dynamo = boto3.client('dynamodb')
    translate = boto3.client('translate')
    polly = boto3.client('polly')

    try:
        query_response = dynamo.get_item(TableName=TABLE_NAME,
                                   Key={
                                        'DictionaryForm': {
                                            'S': event['dictionary_form']
                                        }
                                   })
        print('queryok')
        if 'Item' not in query_response:
            translation = translate.translate_text(Text=event['dictionary_form'],
                                                   SourceLanguageCode='it',
                                                   TargetLanguageCode='en')
            print(f"translateok {translation['TranslatedText']}")
            polly_response = polly.start_speech_synthesis_task(Engine='standard',
                                                               LanguageCode='it-IT',
                                                               OutputFormat='mp3',
                                                               OutputS3BucketName=BUCKET_NAME,
                                                               OutputS3KeyPrefix=f"{event['dictionary_form']}/",
                                                               Text=event['dictionary_form'],
                                                               VoiceId='Giorgio')
            print('pollyok')
            put_response = dynamo.put_item(TableName=TABLE_NAME,
                                           Item={
                                                'DictionaryForm': {
                                                    'S': event['dictionary_form'],
                                                },
                                                'Translation': {
                                                    'S': translation['TranslatedText'],
                                                },
                                                'PronunciationPath': {
                                                    'S': polly_response['SynthesisTask']['OutputUri'],
                                                }
                                           },
                                           ConditionExpression='attribute_not_exists(DictionaryForm)'
                                           )
            print('putitemok')
    except Exception:
        print('Exception')
        return {
            'statuscode': 500,
            'body': json.dumps("Something went wrong")
        }
    return {
        'statuscode': 200,
        'body': json.dumps('OK')
    }
