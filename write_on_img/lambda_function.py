from PIL import Image, ImageDraw, ImageFont
import datetime
import boto3

import os
def get_from_s3(key):
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    localFilename = '/tmp/{}'.format(os.path.basename(key))
    bucket.download_file(key, localFilename)
    return localFilename

def upload_to_s3(filename):
    
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    now = datetime.datetime.now()
    filepath = "{0}/{1}{2}".format(now.strftime("%Y%m%d"),now.strftime("%H"),'img.png')    
    
    s3.Object(os.environ['S3_BUCKET'], filepath).put(Body=open(filename, 'rb'))
    return filepath

def write_on_img(template, text):
    local_font = get_from_s3('assets/Roboto-Regular.ttf')
    local_template = get_from_s3(template)    

    # pass text and location
    img = Image.open(local_template)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(local_font, size=72)

    draw.text((25, 400), "AQI - {0}".format(text),  fill = 'black', font=font)
    path = '/tmp/filled_template.png'
    img.save(path)
    return path

def handler(event, context):
    images_map = {
        'Good': 'assets/good.png',
        'Moderate': 'assets/moderate.png',
        'Unhealthy for Sensitive Groups': 'assets/sensitive.png',
        'Unhealthy': 'assets/unhealthy.png',
        'Very Unhealthy': 'assets/v_unhealthy.png',
        'Hazardous': 'assets/hazardous.png',
        'Extra Hazardous': 'assets/memo_haljevac.jpeg',
    }

    if event['feedData']['last']['aqi'] > 499:
        event['feedData']['last']['desc'] = 'Extra Hazardous'
    
    path = upload_to_s3(write_on_img(images_map[event['feedData']['last']['desc']], event['feedData']['last']['aqi']))
    return {'template_img':path}