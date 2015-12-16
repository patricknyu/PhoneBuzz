from flask import Flask, request, redirect
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
		resp.say("Hello " + callers[from_number])
	else:
		resp.say("Helo Monkey")

	return str(resp)

if __name__ == "__main__":
	app.run(debug=False)
