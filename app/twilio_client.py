from twilio.rest import TwilioRestClient
import os

account = "AC293ba385dfd140435b955c184eb6b7a7"
token = "ae6f6c20e96fc7a9803a100292ab5284"

if(account == "" or token == ""):
	account = os.environ['TWILIO_ACCOUNT']
	token = os.environ['TWILIO_TOKEN']
client = TwilioRestClient(account, token)
