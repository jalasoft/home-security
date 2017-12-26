from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from server import settings
from dashboard.lib.managed_camera import ManagedCamera

import logging

logger = logging.getLogger("camera_endpoints")

managedCamera = ManagedCamera(settings.SNAPSHOT_DIR, settings.AREA_TO_CAMERA_MAPPING)

def captureArea(request, area):  
    if request.method != 'GET':
        return HttpResponseBadRequest("Unexpected method, only GET allowed")
		
    if not managedCamera.supportsArea(area):
        return HttpResponseBadRequest("Unknown area '{}", area)
   
    refresh = __extractRefreshParameter__(request)
    encoding = __extractEncoding__(request)
    
    logger.info("A request arrived for area '{}' refreshing={},encoding={}".format(str(area), str(refresh), encoding))
    
    capturedFile = managedCamera.capture(area, refresh)
    logger.info("A new snapshot obtained: '" + str(capturedFile) + "'.")
    
    b64Content = capturedFile.readString(encoding);
    response = HttpResponse(b64Content, content_type='image/jpeg')
    response["X-SNAPSHOT-CREATED-ISO"] = capturedFile.createdISOTimeString()
    
    return response
    
def __extractRefreshParameter__(request):
    refreshString = request.GET.get('refresh', default='false').lower().strip()
    
    if refreshString == 'true':
        return True
        
    return False

def __extractEncoding__(request):
    encoding = request.GET.get("encoding", default=None)
    
    if encoding == '':
        encoding = None;
        
    return encoding

