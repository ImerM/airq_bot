from twython import Twython
import traceback
import boto3
import os

def publish_to_twitter(filepath, statustext):
    twitter = Twython(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])
    try:

        with open(filepath, 'rb') as img:
            twit_resp = twitter.upload_media(media=img)
            twitter.update_status(status=statustext, media_ids=twit_resp['media_id'])

    except TwythonError as e:
        print(e)

def get_from_s3(key):
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    localFilename = '/tmp/{}'.format(os.path.basename(key))
    bucket.download_file(key, localFilename)
    
    return localFilename

def lambda_handler(event, context):
    try:
        publish_to_twitter(get_from_s3(event['image_path']), '')
    except Exception as e:
        traceback.print_exc()
        raise e