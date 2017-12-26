from dashboard.endpoints.login_endpoints import validateToken
from re import compile
import logging
from server import settings

logger = logging.getLogger("dashboard.middleware.SecurityMiddleware")

class SecurityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.securedPathsPatterns = list(compile(path) for path in settings.SECURED_PATHS)
        
    def __call__(self, request):
        
        logger.debug("Http request obtained: " + request.path)
        
        if not self._shouldValidateSecurityToken(request):
            return self.get_response(request)
        
        logger.debug("Http request is about to be validated.")
        
        
        validationResponse = validateToken(request)
		
        logger.debug("Http request validation ended with status " + str(validationResponse.status_code))
		
        if validationResponse.status_code == 401:
            return validationResponse 
		
        response = self.get_response(request)
        return response
        

    def _shouldValidateSecurityToken(self, request):
        path = request.path
 
        matchingPatterns = list(c for c in self.securedPathsPatterns if c.match(path))
  
        length = len(matchingPatterns)
        willBeValidated = length > 0
        logger.debug("Will be validated: " + str(willBeValidated))
        return willBeValidated
