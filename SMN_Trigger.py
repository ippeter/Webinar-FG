# -*- coding:utf-8 -*-
import json, requests

def handler(event, context):
    """
    Function triggers when Cloud Eye sends a notification to SMN
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
    data = json.loads(event['record'][0]['smn']['message'])
    ecs_id = data["dimension"].split(":")[1]
    logger.info(ecs_id)

    # Build Header and Body of the POST request
    hdr = {'Content-Type': 'application/json;charset=utf8', 'X-Auth-Token': token}
    bdy = json.dumps({ "os-stop": {} })

    # Do POST request
    resp = requests.post("https://ecs.ru-moscow-1.hc.sbercloud.ru/v2.1/" + project_id + "/servers/" + ecs_id + "/action", headers=hdr, data=bdy)

    return resp.status_code
