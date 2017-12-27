from django.http import HttpResponse

import logging
from server import settings
from dashboard.endpoints.jwt import WebTokenError
from dashboard.application import securityTokenProcessor, blackListedTokens

logger = logging.getLogger("login_endpoints")

def login(request):
    
    if request.method != 'POST':
        return HttpResponseBadRequest("Unexpected method, only POST allowed")
        
    password = request.body.decode("utf-8")
    
    logger.info("Loging for password '{}'".format(password))
    
    if password != settings.PASSWORD:
        return HttpResponse(status=401);
             
    response = HttpResponse();
    securityToken = securityTokenProcessor.generateToken({}, settings.SECURITY_TOKEN_VALIDITY_SECONDS)
    logger.info("A new security token generated: {}".format(securityToken))
    
    response['X-SECURE-TOKEN'] = securityToken.value()
    
    return response;

def logout(request):
    token = request.META["HTTP_X_SECURE_TOKEN"]
    blackListedTokens.append(token)
    
    logger.debug("Token {} has been black-listed.".format(token))
    
    return HttpResponse(status=200)

def validateToken(request):
    
    token = request.META["HTTP_X_SECURE_TOKEN"]
    
    logger.info("Verifying token '{}'".format(token))
    
    if token is None:
        return HttpResponse(status=401)
    
    if token in blackListedTokens:
        return HttpResponse(status=401)
         
    try:
        securityToken = securityTokenProcessor.parseToken(token)
    
        if securityToken.isExpired():
            return HttpResponse(status=401) 
    except WebTokenError as e:
        logger.error(e);
        return HttpResponse(status=401)
        
    return HttpResponse(status=200)
