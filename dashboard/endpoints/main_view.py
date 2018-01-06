from django.shortcuts import render
from django.http import HttpResponse
from server import settings

import logging

logger = logging.getLogger("main_view")

def dashboard(request):
    context = {
        'areas' : settings.AREA_TO_CAMERA_MAPPING.keys()
    }
    
    logger.debug("Rendering web page content.")
    
    return render(request, 'dashboard/main.html', context) 
