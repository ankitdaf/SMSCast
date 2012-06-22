#!/usr/bin/env python

import cgi
import urllib
import urllib2
import datetime
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

head = '<html><head>'
txtweb_appkey='Your app key here'	# Edit only this
meta = "<meta name=\'txtweb-appkey\' content=\'%s\'/>"%(txtweb_appkey)
body = "</head><body>"
end = "</body></html>"
pubkey = 'Your publisher key here'	#Also edit this

def write_mobile_header(self):
	"""
	Headers to be sent as per txtweb API
	"""
	self.response.out.write(head)
	self.response.out.write(meta)
	self.response.out.write(body)

def write_web_header(self):
	"""
	Headers to be sent in case its a browser
	Don't write the appkey
	"""
	self.response.out.write(head)
	self.response.out.write(meta)	# Enable this in order to publish the app, or it wont work.Unfortunate but necessary
	self.response.out.write(body)

def end_html(self):
	"""
	Close the HTML response
	"""
	self.response.out.write(end)

def get_cusswords(): 
	"""
	Makes a list for bad words filter
	"""
	f = open('badwords.txt','r')
	cuss_words = [i.replace('\n','').replace('\r','') for i in f]
	return cuss_words

class Users(db.Model):
	"""
	Models a User entry with cellphone number and chosen username
	"""
	date = db.DateTimeProperty(auto_now_add = True)
	username = db.StringProperty( multiline = False)
	mobile = db.StringProperty()

def userlist_key():
	"""
	Constructs a datastore key for a Userlist table with userlist as its name
	"""
	return db.Key.from_path('Userlist', "userlist")

def get_mobile():
	"""
	Get a list of txtweb-mobiles registered
	"""
	users = Users.gql("")
	mobile_list = [i.mobile for i in users]
	return mobile_list

def verify_source(verifyid,message,sender,protocol):
	"""
	Verify if the request indeed came from txtweb
	Prevents potential web spamming attacks
	"""
	arguments = {"txtweb-verifyid":verifyid,"txtweb-message":message,"txtweb-mobile":sender, "txtweb-protocol":protocol}
	encoded_arguments = urllib.urlencode(arguments)
	url="http://api.txtweb.com/v3/verify" + "?" + encoded_arguments
	result = urlfetch.fetch(url)
	if("success" in result.content):
		return True
	else:
		return False

def get_username():
	"""
	Get a list of all registered usernames
	"""
	users = Users.gql("")
	user_list = [i.username for i in users]
	return user_list


class MainPage(webapp.RequestHandler):
	"""
	Handles calls to the app
	"""
	def get(self):
		"""
		Serves GET requests made by txtweb
		"""
		self.response.headers["Content-Type"] = 'text/html'
		message = cgi.escape(self.request.get('txtweb-message')) #get hold of txtweb-message here
		sender = self.request.get('txtweb-mobile')
		verifyid= self.request.get('txtweb-verifyid')
		protocol = self.request.get('txtweb-protocol')
		cuss_words = get_cusswords()
		cuss_pr = [i for i in cuss_words if i in message]	#check the message for bad words
		if (verify_source(verifyid,message,sender,protocol) and (not cuss_pr)):
			write_mobile_header(self)
			msg=message.split()
			if(len(msg)==0):
				self.response.out.write('You forgot to enter a message,Saar')
			elif("register" in msg[0]):
				try:
					username = msg[1]			#registers a particular user for the sms notification service
					user = Users(parent = userlist_key())
					mobile_list = get_mobile()
					user_list = get_username()
					if sender in mobile_list:
						self.response.out.write("You are already registered,Saar")
					elif username in user_list:
						self.response.out.write("Username is already taken,Saar. Please choose another username and register again")
					else:
						user.username = username
						user.mobile = sender
						user.put()
						self.response.out.write('You have registered successfully, %s'%(username))
						self.response.out.write(' To send messages to this group, just send @coffeekatta Your_message to the same number')
				except IndexError:
					self.response.out.write("You need to enter a username also,Saar")
			else:
					users = Users.gql("")
					mobile_list = get_mobile()
					is_allowed=False
> 				this_sender=""
> 				for user in users:
> 					if (sender in user.mobile):
							is_allowed=True
> 						this_sender=user.username
							break
					if is_allowed:
 						htmlresponse = head + meta + body + this_sender+": " + message + end
						for user in users:
							form_fields = {"txtweb-mobile":user.mobile, "txtweb-message":htmlresponse, "txtweb-pubkey":pubkey}
							form_data = urllib.urlencode(form_fields)
							result = urlfetch.fetch(url="http://api.txtweb.com/v1/push",payload=form_data,method=urlfetch.POST)
> 						if(not ("success" in result.content)):
> 							logging.info(user.username)
> 							logging.info(result.content)
						self.response.out.write("Bhej diya, Saar ")
					else:
						self.response.out.write("Message bhejna manaa hai, Saar")
		else:
			write_web_header(self)
			self.response.out.write('Nahi Chalega, Saar')
		end_html(self)

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()