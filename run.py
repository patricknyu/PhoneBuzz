from flask import Flask, request, redirect, render_template
import time
from twilio.rest import TwilioRestClient
#from __future__ import with_statement
import twilio.twiml
import validator
import twilio_client

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

"""@app.route("/hello_monkey",methods = ['GET','POST'])
def hello_monkey():

	#Get the callers number
	from_number = request.values.get('From',None)
	resp = twilio.twiml.Response()
	
	#check if the caller is someone we know
	if from_number in callers:
		caller = callers[from_number]
	else:
		caller = "Monkey"
	
	resp.say("Hello " + caller)
	#Play an MP3
	resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")
	
	with resp.gather(finishOnKey = '#', action = "/handle-key",method= "POST") as g:
		g.say("Press a number. Then press pound.  I will return Fizz Buzz up to that number.")
	return str(resp)
"""
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

	callRequests[currentTime] += (digit_pressed,)

	"""if digit_pressed == "1":
		resp = twilio.twiml.Response()
		resp.dial("+13105551212")
		resp.say("The call failed, or the remote party hung up.  Goodbye.")

		return str(resp)
	else:
		return redirect("/")"""
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
	currentTime = time.strftime('%d.%m.%Y%I.%M.%S')
	history.append(currentTime)
	callRequests[currentTime] = (delay,num)
	time.sleep(int(delay))
	#print(request.url_root+"call?time="+currentTime)
	# Make the call
	client.calls.create(to=num,  # Any phone number
	from_="5167145942", # Must be a valid Twilio number
	url=request.url_root+"call?time="+currentTime)
	
	return ""

if __name__ == "__main__":
	app.run(debug=False)
