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
	url = 'http://www.quizlet.com/'
	answer_dict = {}
	assignment_number = None
	driver = None

	def __init__ (self):
		self.driver = webdriver.Firefox()
		self.setup()
		self.scrap_site()
		self.selector()

	def setup (self):

		driver = self.driver
		driver.get(self.url)
		driver.find_element_by_css_selector('div[class^="login poppable clickable"]').click()
		driver.implicitly_wait(3)

		username = 'hmeteke'
		password = 'Inturn77!'
			
		user = driver.find_element_by_name('username')
		user.click()
		user.clear()
		user.send_keys(username)
		
		passwd = driver.find_element_by_name('password')
		passwd.click()
		passwd.clear()
		passwd.send_keys(password)
		
		driver.find_element_by_css_selector('[class^="submit button"]').click()

		self.assignment_number = raw_input('>')
		
	def scrap_site(self):
		driver = self.driver
		answer_dict = {}
		driver.get(self.url + self.assignment_number)
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
		learner_url = self.url + self.assignment_number + '/learn'
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
			except KeyError:
				continue	
			except NoSuchElementException:
				try:
	
					remainder = driver.find_element_by_css_selector("*[class^='LearnModeSidebar-counterNumber']").text

					try:
						if 'Correct' == driver.find_element_by_css_selector("*[class^='LearnModeTitle LearnModeTitle--correct']").text:

							driver.find_element_by_xpath('//body').send_keys(Keys.RETURN)
							print remainder + ' more questions'

					except NoSuchElementException:
						if 'Incorrect' == driver.find_element_by_css_selector("*[class^='LearnModeTitle LearnModeTitle--incorrect']").text:
							print 'overrode'
							driver.find_element_by_css_selector("*[class^='LearnModeGradeAnswerView-overrideButton']").click()

					if int(remainder) == 0:
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

		speller_url = self.url + self.assignment_number + '/speller'
		driver.get(speller_url)
		
		select_speed = Select(driver.find_element_by_id('speller-prompt'))
                select_speed.select_by_visible_text("Don't Speak")
                alert = driver.switch_to_alert()
                alert.accept()
		driver.implicitly_wait(3)
		counter = 0
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
				completed = driver.find_element_by_id('overall-percent').text
				print completed + '% completed'	
			
			except TimeoutException:
				print 'Timeout'
				continue

			except NoSuchElementException:
				counter += 1
				if driver.find_element_by_id('game-over').text == "Congratulations, you're done!":
					print 'FINISHED'
					break
				elif counter == 3:
					driver.get(speller_url)
				else:
					print 'Reloading'	
					continue
	
	def selector (self):
		while True:
			choice = int(raw_input('1) Learner\n2) Speller\n>'))
			if choice == 1:
				self.do_learner()
			if choice == 2:
				self.do_speller()
			else:
				print 'ERROR WRONG CHOICE'

start = AutoApp()
