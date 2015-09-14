from threading import Thread
import selenium
from selenium import webdriver
import time


class FakeAccount(Thread):

	driver     = None
	address    = None

	def __init__(self):
		super(FakeAccount, self).__init__()

	def run(self):
		self.driver = webdriver.Chrome()
		self.driver.delete_all_cookies()
		self.make_fake_email()
		#time.sleep(30)
		#self.driver.close()

	def make_fake_email(self):
		self.driver.get("http://www.fakeinbox.com/")
		self.driver.find_element_by_name("getemail").click()
		self.address = self.driver.find_element_by_name("mail").get_attribute("value")

	def get_email_address(self):
		return self.address

	def check_emails_by_subject(self,subject_content):
		#search by subject_content
		return "" #email content

	def get_driver(self):
		return self.driver

	def get_email_body(self):
		flag1 = True
		while flag1:
			try:
				self.driver.find_element_by_xpath("//a[@href='./']").click()
				self.driver.find_element_by_xpath("//a[contains(text(), 'Show')]").click()
				flag1 = False
			except selenium.common.exceptions.NoSuchElementException:
				time.sleep(.01)
				continue
		flag2 = True
		#page = self.driver.find_element_by_xpath("//td[@class='t12l_mail_details_text']").get_attribute("innerHTML")

		while flag2:
			try:
				return self.driver.find_element_by_xpath("//td[@class='t12l_mail_details_text']").get_attribute("innerHTML")
				flag2 = False
			except selenium.common.exceptions.NoSuchElementException:
				continue

	def kill(self):
		self.driver.close()

class EmailManager:

	account_list = None

	def __init__(self):
		self.account_list = []

	def create_accounts(self,no_of_accounts):
		print "[EmailManager] Creating %i fake email accounts..." % no_of_accounts
		for i in range(1,no_of_accounts+1):
			new_account = FakeAccount()
			self.account_list = self.account_list + [new_account]
			print "[EmailManager] Making Fake Account %i" % i
			new_account.start()
			time.sleep(.05)
		print "[EmailManager] Waiting for cows to come home..."
		while not self.is_done_creating_accounts():
			pass
		print "[EmailManager] %i account(s) made: \n" % len(self.account_list)
		for i in self.account_list:
			print "    %s" % i.get_email_address()
		print "\n[EmailManager] All cows came back home"

	def is_done_creating_accounts(self):
		for account in self.account_list:
			if account.get_email_address() is None:
				return False
		return True

	def get_account_list(self):
		return self.account_list

	def thread_task(self,account,bodies):
		bodies.append(account.get_email_body())

	def get_emails(self):
		print "[EmailManager] Checking emails"
		bodies = []
		for i in self.account_list:
			#self.thread_task(i,bodies)
			Thread(target=self.thread_task,args=(i,bodies)).run() #gotta figure this out
		return bodies

	def killall(self):
		for i in self.account_list:
			i.kill()
