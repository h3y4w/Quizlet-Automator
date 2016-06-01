from pyvirtualdisplay import Display
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class AutoApp (object):
	email = None
	password = None	
	answer_dict = {}
	assignment_number = None
	user = None
	driver = None
	def __init__ (self):
		self.driver = webdriver.Firefox()
		self.user = 'deno'
		self.setup()
		self.scrap_site()
		self.selector()

	def setup (self):
		driver = self.driver		
		with open('accounts/' + self.user + '/quizlet') as f: #Gets user's email and password from their file
			temp_userInfo = f.readlines()
			temp_userInfo = unicode(''.join(temp_userInfo), 'utf-8') #turns it into utf
			index = temp_userInfo.find(':')
			self.email = temp_userInfo[:index]
			self.password = temp_userInfo[index+1:]		
			print temp_userInfo[index+1:]

		with open('loginLink.txt') as f:
			temp_loginLink = f.readlines()
		loginLink = unicode(''.join(temp_loginLink), 'utf-8')
		driver.get(loginLink)
	
		email = driver.find_element_by_name('Email')
		email.click()
		email.send_keys(self.email)
		driver.find_element_by_name('signIn').click()
		
		driver.implicitly_wait(5)

		password = driver.find_element_by_name('Passwd')
		password.click()
		password.send_keys(self.password)
		
		self.assignment_number = raw_input('>')
		
	def scrap_site(self):
		driver = self.driver
		answer_dict = {}
		url = 'https://quizlet.com'
		driver.get(url + '/' + self.assignment_number)
		driver.get(driver.current_url + 'alphabetical')

		source = (driver.page_source)
		def_found = 0
		def_index = 0
		ans_found = 0
		ans_index = 0
		temp_index_ans = 0
		temp_index_def = 0
		while temp_index_ans != 14 and temp_index_def != 13:
			temp_index_ans = source.find('qWord', ans_index)+15
			ans_index = temp_index_ans
			temp_ans = source[temp_index_ans:]
			qWord = temp_ans.split('<')
			qWord = qWord[0]

			temp_index_def = source.find('qDef', def_index)+14
			def_index = temp_index_def
			temp_def = source[temp_index_def:]
			qDef = temp_def.split('<')
			qDef = qDef[0]

			answer_dict[qDef]=qWord
		
		self.answer_dict = answer_dict

	def do_learner (self):
		driver = self.driver
		learner_url = 'https://quizlet.com/' + self.assignment_number + '/learn'
		driver.get(learner_url)		
		answer_dict = self.answer_dict	
		counter = 0
		while True:
			try:
			
				driver.implicitly_wait(3)
				question = driver.find_element_by_css_selector("*[class^='qDef lang-en TermText']").text
				inputA = driver.find_element_by_id('user-answer')
				inputA.click()
				inputA.clear()
				inputA.send_keys(answer_dict[question])
				buttonA = driver.find_element_by_id('answer-button')
				buttonA.click()

			except TimeoutException:
				driver.get(learner_url)
			
			except NoSuchElementException:
				try:
	
					remainder = driver.find_element_by_css_selector("*[class^='LearnModeSidebar-counterNumber']").text
					if 'Correct' == driver.find_element_by_css_selector("*[class^='LearnModeTitle LearnModeTitle--correct']").text:
						driver.get(learner_url)
						print remainder + ' more questions'

					elif 'Incorrect' == driver.find_element_by_css_selector("*[class^='LearnModeTitle LearnModeTitle--incorrect']").text:
						driver.find_element_by_css_selector("*[class^='LearnModeGradeAnswerView-overrideButton']").click()

					elif int(remainder) == 0:
						print 'Finished!'
						break
				except NoSuchElementException:
					counter += 1
					if counter == 3:
						break
					else:
						continue



	def do_speller (self):
		driver = self.driver
		answer_dict = self.answer_dict

		speller_url = "https://quizlet.com/" + self.assignment_number + '/speller'
		driver.get(speller_url)
		
		select_speed = Select(driver.find_element_by_id('speller-prompt'))
                select_speed.select_by_visible_text("Don't Speak")
                alert = driver.switch_to_alert()
                alert.accept()
		driver.implicitly_wait(3)
		while True:
			try:
				driver.implicitly_wait(3)
				question=driver.find_element_by_css_selector("*[class^='qDef lang-en TermText']").text
               		 	inputA = driver.find_element_by_id('speller-inp')
				inputA.click()
				inputA.clear()
				inputA.send_keys(answer_dict[question])
                		inputA.send_keys(Keys.RETURN)
				driver.get(speller_url)
				completed = driver.find_element_by_id('prograssbar-sm').text
				print completed + '% completed'	
			
			except TimeoutException:
				print 'Timeout'
				continue

			except NoSuchElementException:
				
				if driver.find_element_by_id('game-over').text == "Congratulations, you're done!":
					print 'FINISHED'
					break
				else:
					print 'Reloading'	
					continue
	
	def selector (self):
		choice = 1
		while True:
			if choice == 1:
				self.do_learner()
			if choice == 2:
				self.do_speller()
			else:
				print 'ERROR WRONG CHOICE'

start = AutoApp()
