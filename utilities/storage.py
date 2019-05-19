import datetime
import os
import six

from flask import current_app
from google.cloud import storage

def upload_image_file(file, folder, content_id):
    if not file:
        return None 
    file.format = 'png'
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    filename = '{}-{}.{}'.format(content_id, date, 'png')
    
    client = storage.Client(project = current_app.config['PROJECT_ID'])
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(os.path.join(folder, filename))
    
    blob.upload_from_string(file.read(),
                            content_type = file.content_type)
    url = blob.public_url
    
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')
    return url
    