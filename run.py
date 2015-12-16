from flask import Flask
import twilio.twiml as twmil
app = Flask(__name__)

@app.route("/",methods = ['GET','POST'])
def hello_monkey():
	"""Respond to incoming requests."""
	resp = twiml.Response()
	resp.say("Hello Monkey")

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
