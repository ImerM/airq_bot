import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import boto3
import os
import datetime
import traceback


def make_hist(data):
    dpi = 96
    plt.figure(1,figsize=(700/dpi,500/dpi))
    plt.bar(data['x'], data['y'], color=data['color'])
    ax = plt.gca()
    plt.xticks(rotation=45)
    plt.text(0.5, 1.05, 'Prethodna 24 sata', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize = 16)
    plt.savefig('/tmp/histogram.png')
    return ('/tmp/histogram.png')

def upload_to_s3(filename):
    
    s3 = boto3.resource('s3', region_name=os.environ['REGION_HOST'])
    now = datetime.datetime.now()
    filepath = "{0}/{1}{2}".format(now.strftime("%Y%m%d"),now.strftime("%H"),'hist.png')    
    
    s3.Object(os.environ['S3_BUCKET'], filepath).put(Body=open(filename, 'rb'))
    return filepath

def handler(event, context):
    try:
        path = upload_to_s3(make_hist(event['feedData']['all']))
        return {'hist_img': path}
    except Exception as e:
        traceback.print_exc()
        raise e
