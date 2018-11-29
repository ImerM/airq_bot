from PIL import Image, ImageDraw, ImageFont
import datetime
import boto3
import numpy as np
import os
import traceback

def merge_images(template, histogram):
    # merges two images of identical Y size
    im1 = Image.open(template).convert('RGB')
    r1, g1, b1 = im1.split()

    im2 = Image.open(histogram).convert('RGB')
    r2, g2, b2 = im2.split()

    r = np.concatenate((np.array(r1), np.array(r2)), axis=1)
    g = np.concatenate((np.array(g1), np.array(g2)), axis=1)
    b = np.concatenate((np.array(b1), np.array(b2)), axis=1)

    arr = np.dstack([r, g, b])
    im = Image.fromarray(arr, 'RGB')

    im.save('/tmp/newest.png', facecolor='#FFFFFF', edgecolor='#FFFFFF')

    return '/tmp/newest.png'

def get_from_s3(key):
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    bucket = s3.Bucket(os.environ['S3_BUCKET'])

    localFilename = '/tmp/{}'.format(os.path.basename(key))
    bucket.download_file(key, localFilename)
    return localFilename

def upload_to_s3(filename):
    
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    now = datetime.datetime.now()
    filepath = "{0}/{1}{2}".format(now.strftime("%Y%m%d"),now.strftime("%H"),'merged_image.png')    
    s3.Object(os.environ['S3_BUCKET'], filepath).put(Body=open(filename, 'rb'))
    return filepath

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def handler(event, context):
    try:
        data = merge_two_dicts(event[0], event[1])
        image = get_from_s3(data['template_img'])
        hist = get_from_s3(data['hist_img'])

        path = upload_to_s3(merge_images(image, hist))
        return path
    except Exception as e:
        traceback.print_exc()
        raise e