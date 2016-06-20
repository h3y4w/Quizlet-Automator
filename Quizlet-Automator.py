#!/usr/bin/env python
#############
## ADD A WAY FOR IT TO ELEGANTLY EXIT ##

import easygui as eg
import AQ

class window (object):
	app = None
	window_name = "QUIZLET AUTOMATOR"
	
	def __init__ (self):
	
		self.prompt_login()
		while (True):	
			self.prompt_assignment()
			self.app.scrap_site()
			self.prompt_options()
	def prompt_login (self):

		msg = "QUIZLET LOG IN"
		form_q = ['Username', 'Password']
		while (True):
			user_info = eg.multpasswordbox(msg, self.window_name, form_q)
			if user_info:
				self.app = AQ.AutoApp(user_info)
				if self.app.login():
					break
				else:
					msg= 'Incorrect username/password'	
				
			else:
				exit(1)
	def in_menu (self):
		pass	
	def prompt_assignment (self): 
		upperbound = 999999999999999^2 #temp, setting upperbound to None doesn't work
		msg = 'Type the assignment number, example is shown below'
		image = 'assignment_number_example.png'
		self.app.assignment_number = str(eg.integerbox(msg, self.window_name, upperbound=upperbound, image=image))
			
	def prompt_options (self):	
		buttons = ['Speller', 'Learner', 'Test']
		choice = eg.buttonbox('What lesson would you like to do?', self.window_name, buttons)
		if choice == buttons[0]:
			self.app.do_speller()
			eg.msgbox('Completed Speller', self.window_name)
		if choice == buttons[1]:
			self.app.do_learner()
			eg.msgbox('Completed Learner', self.window_name)			
		if choice == buttons[2]:
			self.app.do_test()
			eg.msgbox('Completed Test', self.window_name)
start = window()
