# Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Get these credentials from http://twilio.com/user/account
account_sid = "AC293ba385dfd140435b955c184eb6b7a7"
auth_token = "ae6f6c20e96fc7a9803a100292ab5284"
client = TwilioRestClient(account_sid, auth_token)
  
# Make the call
call = client.calls.create(to="+17146515438",  # Any phone number
                             from_="+15167145942", # Must be a valid Twilio number
			                                url="https://fathomless-gorge-8817.herokuapp.com")
print call.sid
