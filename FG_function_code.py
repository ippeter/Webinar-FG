# -*- coding:utf-8 -*-
import os
import numpy as np
import random as rd
from PIL import Image

from com.obs.client.obs_client import ObsClient

def handler(event, context):

    ak = context.getAccessKey()
    sk = context.getSecretKey()
    endpoint = "obs.ru-moscow-1.hc.sbercloud.ru"

    logger = context.getLogger()
    bucket_name = event['Records'][0]['obs']['bucket']["name"]
    file_name = event['Records'][0]['obs']['object']["key"]
    file_size = event['Records'][0]['obs']['object']["size"]
    logger.info("File %s received, size is %s" % (file_name, file_size))

    if (file_size > 0):
        conn = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint, path_style=True, region="ru-moscow-1")

        local_incoming_file_name = os.path.join(os.sep, "tmp", file_name)
        resp = conn.getObject(bucket_name, file_name, local_incoming_file_name)

        im = Image.open(local_incoming_file_name)

        original_width, original_height = im.size
        new_width = 200
        new_height = int(original_height * new_width / original_width)

        im.thumbnail((new_width, new_height), Image.ANTIALIAS)

        arr = np.array(np.asarray(im))

        for i in range(3):
            m = rd.choice([-1, 1])
            arr[:, :, i] = arr[:, :, i] + m*50

        result = Image.fromarray(arr)

        local_outgoing_file_name = os.path.join(os.sep, "tmp", "_" + file_name)

        result.save(local_outgoing_file_name)

        resp = conn.putFile("pvc-91c18543-9524-11ea-8dc4-fa163e7f29e7", file_name, local_outgoing_file_name)
        logger.info(resp["status"])

    return "File processed."
