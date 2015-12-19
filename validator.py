from twilio.util import RequestValidator
import os

AUTH_TOKEN = 'ae6f6c20e96fc7a9803a100292ab5284'

if AUTH_TOKEN == '':
	  AUTH_TOKEN = os.environ['TWILIO_TOKEN']

	  validator = RequestValidator(AUTH_TOKEN)

	  def isValid(url, signature, postVars = {}):
	    return validator.validate(url, postVars, signature)
