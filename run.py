from flask import Flask, request, redirect, render_template
import time
from twilio.rest import TwilioRestClient
#from __future__ import with_statement
import twilio.twiml
import validator
import twilio_client
from time import gmtime, strftime
app = Flask(__name__)

callers = {
	"+17146515438": "Patrick",
	"+14158675310": "Boots"}

history = []
callRequests = {}
@app.before_request
def before_request():
  if request.path in ["/call", "/handle-key"]:
	      if (not validator.isValid(request.url, request.headers['X-Twilio-Signature'], request.form)):
		            return "That is invalid"
@app.route('/')
@app.route('/index')
def html_render():
	global history
    	global callRequests
    	return render_template('index.html',history =history,callRequests=callRequests)

@app.route("/call",methods = ["POST"])
def call():
	currentTime = request.args.get('time')
	resp = twilio.twiml.Response()
	with resp.gather(action=("/handle_key?time="+currentTime)) as g:
		g.say("Press a number. Then press pound.  I will return Fizz Buzz up to that number.")
	return str(resp)

@app.route("/handle_key",methods = ['POST'])
def handle_key():
	global callRequests
	digit_pressed = request.form['Digits']
	currentTime = request.args.get('time')

	callRequests[currentTime][2] = digit_pressed

	def int_to_fizzbuzz(i):
		ans = ''
		if(i%3==0):
			ans+="fizz"
		if(i%5==0):
			ans+="buzz"
		if(i%3!=0 and i%5!=0):
			ans = str(i)
		return ans
	resp = twilio.twiml.Response()
	for x in range(1,int(digit_pressed)+1):
		resp.say(str(int_to_fizzbuzz(x)))
	return str(resp)
"""
@app.route("/replay",methods=['POST'])
def replay():
	global history
	global callRequests

	num = request.form['Digits']
	phoneNum = request.form['Phone']

	currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

	history.append(currentTime)
	#delay is 0
	callRequests[currentTime] = [0,phoneNum,-1]
	account_sid = "AC293ba385dfd140435b955c184eb6b7a7"
	auth_token = "ae6f6c20e96fc7a9803a100292ab5284"
	client = TwilioRestClient(account_sid, auth_token)
	
	#create the call similarly to before, just force the digits given.
	client.calls.craete(to=phoneNum, # The given phone number
	from_ = "5167145942", #Tilio number
	url=request.url_root+"call?time="+currentTime,send_digits = num)
	return ""
"""
@app.route("/make_call",methods=["POST"])
def make_call():
	global history
	global callRequests
	# Get these credentials from http://twilio.com/user/account
	account_sid = "AC293ba385dfd140435b955c184eb6b7a7"
	auth_token = "ae6f6c20e96fc7a9803a100292ab5284"
	client = TwilioRestClient(account_sid, auth_token)
	
	num = request.form['phone']
	delay = request.form['delay']
	currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	history.append(currentTime)
	callRequests[currentTime] = [delay,num,-1]
	time.sleep(int(delay))
	#print(request.url_root+"call?time="+currentTime)
	# Make the call
	client.calls.create(to=num,  # Any phone number
	from_="5167145942", # Must be a valid Twilio number
	url=request.url_root+"call?time="+currentTime)
	
	return ""

if __name__ == "__main__":
	app.run(debug=False)
