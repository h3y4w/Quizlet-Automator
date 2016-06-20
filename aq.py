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
import pyttsx
import threading
class speak_thread (threading.Thread):
	engine = None
	def __init__ (self):
		threading.Thread.__init__(self)
		self.engine = pyttsx.init()
	def run (self, phrase):
		self.engine.say(phrase)
    		self.engine.runAndWait()
class AutoApp (object):
	url = 'http://www.quizlet.com/'
	answer_dict = {}
	driver = None
	speak_remainder = None
	assignment_number = None
	user_info = {}
	def __init__ (self, user_info):
		self.user_info = user_info
		self.driver = webdriver.Firefox()
		self.speak_remainder = speak_thread()

	def login (self):

		driver = self.driver
		driver.get(self.url)
		driver.find_element_by_css_selector('div[class^="login poppable clickable"]').click()
		driver.implicitly_wait(3)

		username = self.user_info[0]
		password = self.user_info[1]
			
		user = driver.find_element_by_name('username')
		user.click()
		user.clear()
		user.send_keys(username)
		
		passwd = driver.find_element_by_name('password')
		passwd.click()
		passwd.clear()
		passwd.send_keys(password)
		
		driver.find_element_by_css_selector('[class^="submit button"]').click()

		try: 
			driver.find_element_by_css_selector('section[class^="LoginPage-content"]')
			driver.quit()

		except NoSuchElementException:
			return True
 
	def scrap_site(self):
		driver = self.driver
		answer_dict = {}
		driver.get(self.url + self.assignment_number)
		driver.get(driver.current_url + 'alphabetical')

		source = (driver.page_source)
                f = open('source.txt', 'w')
                f.write((source).encode('utf-8'))
                f.close()
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
	        print answer_dict	
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
				try:
					inputA.click()
                                        break
                                except:
                                    pass
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
							if int(remainder) % 10 == 0 and int(remainder) != 0:
								phrase = remainder + ' more questions'
								self.speak_remainder.run(phrase)

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
		try:
			alert = driver.switch_to_alert()
			alert.accept()
		except NoAlertPresentException:
			pass
		driver.implicitly_wait(3)
		counter = 0
		while True:
			try:
				driver.implicitly_wait(3)
				question=driver.find_element_by_css_selector("*[class^='qDef lang-en TermText']").text
				inputA = driver.find_element_by_id('speller-inp')
				time.sleep(.5)
				try: # this throws an exception when its done
					inputA.click()
				except: #specify element is not visible exception
					self.speak_remainder.run('Finished Speller')
					break
				inputA.clear()
				inputA.send_keys(answer_dict[question])
				inputA.send_keys(Keys.RETURN)
				driver.get(speller_url)
				completed = driver.find_element_by_id('overall-percent').text
				 
				try:
					completed = int(completed.replace('%', ''))
					if completed % 10 == 0 and completed != 0: 
						phrase = completed + ' completed'
						self.speak_remainder.run(phrase) 
				except ValueError:
					continue
				except TypeError:
					continue

			except TimeoutException:
				print 'Timeout'
				continue

			except NoSuchElementException:
				counter += 1
				try:
					if driver.find_element_by_id('game-over').text != "":
						self.speak_remainder.run('Finished Speller')
						break
				except NoSuchElementException:
					continue
				if counter == 3:
					print 'stuck'
				else:
					print 'Reloading'	
					continue
	def do_test (self):
		driver = self.driver
		test_url = self.url + self.assignment_number + '/test'
		driver.get(test_url)

		written  = driver.find_element_by_xpath('//*[@id="written1"]')
		div = written.find_elements_by_tag_name('li')
		for li in div:
			question = li.find_element_by_css_selector('span[class^="TermText qDef lang-en"]').text
			item_id = li.find_element_by_css_selector('label[class^="halfblock"]').get_attribute('for')
			
			inputA = li.find_element_by_id(item_id)	
			inputA.click()
			inputA.clear()
			inputA.send_keys(self.answer_dict[question])
		
		mult_choice = driver.find_element_by_xpath('//*[@id="mult_choice1"]')
		div = mult_choice.find_elements_by_tag_name('li')
		for li in div:
			item_id = li.get_attribute('id')
			#question = 
			block = li.find_element_by_css_selector('ol[class^="letters doubleblock"]')
			counter = 0
			for choice in block:
				sel = '-' + str(counter)
			print 	choice.find_element_by_css_selector('span[class^="TermText qWord lang-es"]').text
					
