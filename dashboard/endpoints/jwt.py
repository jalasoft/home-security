import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
from json import dumps, loads
from enum import Enum
from uuid import uuid4
import logging

logger = logging.getLogger("jwt")

class WebTokenError(Exception):
		
    def __init__(self, resultType):
        self.resultType = resultType

class WebToken:
    def __init__(self, payloadDict, token):
        self.payloadDict = payloadDict
        self.token = token
        self.parts = token.split(".")
        
    def head(self):
        return self.parts[0]

    def payload(self):
        return self.parts[1]
       
    def signature(self):
        return self.parts[2]
                   
    def isExpired(self):
        expiration = int(self.payloadDict["exp"]);
        now = datetime.datetime.utcnow().timestamp()
        
        return now > expiration 

    def value(self):
        return self.token
               
    def __str__(self):
        return "JWT[" + self.token + "]"
    
class _JsonProcessor:
        
    def toJsonBase64UrlEncoded(self, dictionary):
        jsonized = dumps(dictionary)
        b64url = urlsafe_b64encode(jsonized.encode('UTF-8'))
        return b64url.decode('UTF-8')
       
    def fromJsonBase64UrlEncoded(self, string):
        pureJson = urlsafe_b64decode(string)
        dictionary = loads(pureJson.decode("UTF-8"))
        return dictionary

        
class SecurityWebTokenProcessor:

    def __init__(self, secret=None, alg="HS256"):
        self.alg = alg
        self.secret = self._deriveSecret(secret)
        self.jsonProcessor = _JsonProcessor()

    def _deriveSecret(self, secret):
        if not secret is None:
            return secret.encode("UTF-8")
        
        generated = uuid4().bytes
        return generated
        
    def generateToken(self, infoDict, durabilitySeconds):

        headerDict = {
            "alg": self.alg,
            "type": "JWT"
        }

        payloadDict = {
            "exp": self.__computeExpirationMillis(durabilitySeconds)
        }
        payloadDict = {**payloadDict, **infoDict}

        message = self.__prepareMessage(headerDict, payloadDict)

        signature = self.__sign_by_hmac(message, self.secret)
        result = message + "." + signature
        
        return WebToken(payloadDict, result)

    def __prepareMessage(self, headDict, payloadDict):
        header = self.jsonProcessor.toJsonBase64UrlEncoded({
            "alg": self.alg,
            "type": "JWT"
        });        
        payload = self.jsonProcessor.toJsonBase64UrlEncoded(payloadDict)
        return header + "." + payload

    def __computeExpirationMillis(self, durabilitySeconds):
        from datetime import timedelta, datetime

        delta = timedelta(seconds=durabilitySeconds)
        expirationDateTime = datetime.utcnow() + delta
        return expirationDateTime.timestamp()

    def __sign_by_hmac(self, message, secret):
        from hmac import new

        messageBytes = message.encode('UTF-8')

        result = new(key=secret, msg=messageBytes, digestmod='SHA256')
        dig = result.hexdigest()
        return dig

    def parseToken(self, token):
 		
        parts = token.split(".")
         
        if len(parts) != 3:
            raise WebTokenError("WebToken invalid")
        
        head = parts[0]
        body = parts[1]     
     
        try:
            headDict = self.jsonProcessor.fromJsonBase64UrlEncoded(head)
            payloadDict = self.jsonProcessor.fromJsonBase64UrlEncoded(body)
        except TypeError as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise WebTokenError("Token is in an invalid format")
                
        if not self.__isHeadValid(headDict):
                raise WebTokenError("Head is invalid")
        
        if not self.__isPayloadValid(payloadDict):
            raise WebTokenError("Payload is invalid")
        
        message = self.__prepareMessage(headDict, payloadDict)
        actualSignature = parts[2]
        
        if not self.__isSignatureValid(message, actualSignature):
            raise WebTokenError("Signature is invalid");
        
        return WebToken(payloadDict, token)    
       
       
    def __isHeadValid(self, headDict):
        if not "type" in headDict:
            return False
		
        if not headDict["type"] == "JWT":
           return False
        
        if not "alg" in headDict:
            return False
            
        if not headDict["alg"] == self.alg:
            return False   
        return True
        
    def __isPayloadValid(self, payloadDict):
        if not "exp" in payloadDict:
            return False
        return True
            
            
    def __isSignatureValid(self, message, actualSignature):
        constructedSignature = self.__sign_by_hmac(message, self.secret)
        return constructedSignature == actualSignature
 


if __name__ == "__main__":
    processor = SecurityWebTokenProcessor()
    token = processor.generateToken({ "user": "Honzales"}, 30)
    payload = processor.parseToken(token.token)

    print(str(token))
    print(payload)
    print(bool(payload.isExpired()))
