from django.shortcuts import render
from django.http import HttpResponse

import logging

logger = logging.getLogger("main_view")

def dashboard(request):
    context = {
        'title' : 'Kurnik 4.0'
    }
    
    logger.debug("Rendering web page content.")
    
    return render(request, 'dashboard/main.html', context) 
