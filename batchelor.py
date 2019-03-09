from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from os import path
import re
import time

class Batchelor:

	def __init__(self, url, name, margin):
		self.url = url
		self.name = name
		self.margin = margin
		self.digit_regex = re.compile(r"\d+")

		self.selenium_options = Options()
		self.selenium_options.headless = False

	def load_driver(self):
		self.driver = webdriver.Chrome(options=self.selenium_options, executable_path='./chromedriver.exe')

	def close_driver(self):
		self.driver.close()

	def start(self):
		self.added_score = 0

		while True:
			self.load_driver()
			self.load_page()
			self.close_stupid_popups()
			self.process_poll()
			results = self.check_lead()

			if not self.is_lead_sufficient(results):
				votes_to_add = self.calculate_votes_required_for_lead(results)
				
				print("Adding " + str(votes_to_add) + " votes to " + self.name + "'s score \n")
				self.prepare_page()
				for i in range(0, votes_to_add):
					i
					print("Adding vote " + str(i) + " of " + str(votes_to_add))
					self.process_poll()
					self.prepare_page()
				
				self.added_score += votes_to_add
			
			print("Added " + str(self.added_score) + " votes to " + self.name + "'s score so far.")
			time.sleep(60 * 5)
	
	def load_page(self):
		self.driver.get(self.url)
		time.sleep(10)

	def reload_page(self):
		self.driver.refresh()

	def clear_cookies(self):
		self.driver.delete_all_cookies()

	def prepare_page(self):
		self.clear_cookies()
		self.close_driver()
		time.sleep(2)
		self.load_driver()
		self.load_page()
		self.close_stupid_popups()

	def close_stupid_popups(self):
		try:
			surveymonkey = self.driver.find_element_by_class_name("smcx-modal-close")
			surveymonkey.click()
			
			tab_banner = self.driver.find_element_by_class_name("mc-closeModal")
			tab_banner.click()

			cookie_banner = self.driver.find_element_by_css_selector(".optanon-alert-box-button-middle.accept-cookie-container")
			cookie_banner.click()
			
			time.sleep(2)
			again_stupid_mailchimp = self.driver.find_element_by_class_name("mc-modal-bg")
			again_stupid_mailchimp.click()
		except:
			return
	
	def process_poll(self):
		poll_group = self.driver.find_elements_by_css_selector(".css-answer-group.pds-answer-group")
		poll_element = None
		for group in poll_group:
			if self.name in group.text:
				poll_element = group
				break

		if poll_element is None:
			raise NoSuchElementException()

		#input_element = self.driver.find_element_by_css_selector("input.css-radiobutton.pds-radiobutton")
		input_element = poll_element.find_element_by_css_selector("input.css-radiobutton.pds-radiobutton")
		input_element.click()
		vote_element = self.driver.find_elements_by_css_selector(".css-vote-button.pds-vote-button")[0]
		vote_element.click()
		time.sleep(5)

	def check_lead(self):
		poll_results = self.driver.find_elements_by_class_name("pds-feedback-group")
		results = {}
		
		print("Scores: \n")
		for result in poll_results:
			victim = result.find_element_by_class_name("pds-answer-text")
			score_raw = result.find_element_by_class_name("pds-feedback-votes")
			score_split = self.digit_regex.search(score_raw.text)
			score_string = score_split.group(0)
			score = int(score_string)
			results[victim.text] = score

			print(victim.text+ ": " + score_string)
		
		print(results)
		return results

	def is_lead_sufficient(self, results):
		target_lead = results[self.name] * (1 - self.margin)

		for key, result in results.items():
			if result >= target_lead:
				return False
		
		return True

	def calculate_votes_required_for_lead(self, results):
		target_lead = results[self.name] * (1 - self.margin)
		nearest_victim = 0

		for key, result in results.items():
			if result > nearest_victim and not self.name in key:
				nearest_victim = result
		
		# add a few extra
		votes_to_add = (results[self.name] * (1 + self.margin)) - results[self.name]
		return round(votes_to_add)


		
		
		
	
