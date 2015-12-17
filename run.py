from flask import Flask, request, redirect
#from __future__ import with_statement
import twilio.twiml

app = Flask(__name__)

callers = {
	"+17146515438": "Patrick",
	"+14158675310": "Boots"}

@app.route("/",methods = ['GET','POST'])
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
@app.route("/handle-key",methods = ['GET','Post'])
def handle_key():
	digit_pressed = request.values.get('Digits',None)
	"""if digit_pressed == "1":
		resp = twilio.twiml.Response()
		resp.dial("+13105551212")
		resp.say("The call failed, or the remote party hung up.  Goodbye.")

		return str(resp)
	else:
		return redirect("/")"""
	def int_to_fizzbuzz(i):
		ans = ''
		if (i %3==0):
			ans +="fizz"
		if(i%5==0):
			ans+="buzz"
		if(i%3!=0 and i%5!=0):
			ans = i
		return ans
	resp = twilio.twiml.Response()
	for x in range(1,int(digit_pressed)+1):
		resp.say(str(int_to_fizzbuzz(x)))
	return str(resp)


if __name__ == "__main__":
	app.run(debug=False)
