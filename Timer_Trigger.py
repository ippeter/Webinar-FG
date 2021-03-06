# -*- coding:utf-8 -*-
import json, requests

def handler(event, context):
    """
    Function triggers when Timer alarms
    Input:
        event: JSON-structure with details of the event which triggered the function
        context: security context of the function
    Output:
        it's optional (we will return HTTP POST request code)
    """

    # Get security token and project id from the security context 
    token = context.getToken()                                                  # Obtains a token for the tenant. The token will be valid for 24 hours. An agency is required to access IAM.
    project_id = context.getProjectID()                                         # Obtains a project ID.

    # Set up logger and output project id
    logger = context.getLogger()
    logger.info("About to start the ECS in project %s" % project_id)

    # Build Header and Body of the POST request
    hdr = {'Content-Type': 'application/json;charset=utf8', 'X-Auth-Token': token}
    bdy = json.dumps({ "os-start": {} })

    # Do POST request
    resp = requests.post("https://ecs.ru-moscow-1.hc.sbercloud.ru/v2.1/" + project_id + "/servers/7964b9cc-bc4e-4014-aad3-f739915058d8/action", headers=hdr, data=bdy)

    return resp.status_code

