# -*- coding:utf-8 -*-
import os
import numpy as np
import random as rd

# PIL library comes as a dependancy
from PIL import Image

# Internal library to work with Object Storage
from com.obs.client.obs_client import ObsClient

def handler(event, context):
    """
    Function triggers each time there is a new object created in the Object Storage bucket
    Input:
        event: JSON-structure with details of the event which triggered the function
        context: security context of the function
    Output:
        it's optional (we will return a completion message string)
    """
    
    # Get Access Key/Secret Key to work with OBS from the security context 
    ak = context.getAccessKey()
    sk = context.getSecretKey()
    
    # Set up endpoint for OBS
    endpoint = "obs.ru-moscow-1.hc.sbercloud.ru"

    # Get bucket name from environment where 
    # We will upload modified files there
    static_bucket_name = os.environ["STATIC_BUCKET_NAME"]

    # Set up logger
    logger = context.getLogger()
    
    # Get bucket name, file name and file size from the event details
    bucket_name = event['Records'][0]['obs']['bucket']["name"]
    file_name = event['Records'][0]['obs']['object']["key"]
    file_size = event['Records'][0]['obs']['object']["size"]
    logger.info("File %s received, size is %s" % (file_name, file_size))

    # We will only process files of non-zero size
    if (file_size > 0):
        # Open connection to OBS
        conn = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint, path_style=True, region="ru-moscow-1")

        # Construct the local path of the incoming file
        local_incoming_file_name = os.path.join(os.sep, "tmp", file_name)
        
        # Download the file from the bucket
        resp = conn.getObject(bucket_name, file_name, local_incoming_file_name)

        # Open the image
        im = Image.open(local_incoming_file_name)

        # Thumbnail the image 
        original_width, original_height = im.size
        new_width = 200
        new_height = int(original_height * new_width / original_width)

        im.thumbnail((new_width, new_height), Image.ANTIALIAS)

        # Convert the image to Numpy array
        arr = np.array(np.asarray(im))

        # Change colors randomly
        for i in range(3):
            m = rd.choice([-1, 1])
            arr[:, :, i] = arr[:, :, i] + m*50

        # Convert back to image
        result = Image.fromarray(arr)

        # Construct the local path of an updated image
        local_outgoing_file_name = os.path.join(os.sep, "tmp", "_" + file_name)

        # Save updated image
        result.save(local_outgoing_file_name)

        # Upload updated file to another bucket
        resp = conn.putFile(static_bucket_name, file_name, local_outgoing_file_name)
        logger.info(resp["status"])

    return "File processed."
