#MAIN
from emailcreation import *
import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


def get_email_from_body(text):
	first = text.find("href=") + 6
	last = text.find("\" target=\"")
	return text[first:last]

def make_batch_script(no,link):
	if not os.path.exists("run_scripts"):
		os.makedirs("run_scripts")
	new_file = open("run_scripts/account%i.bat" % no,"w")
	'''new_file.write("Dropbox Link:\n\n %s\n\n" % link)
	new_file.write("Password:\n\n asdf")'''
	new_file.write("@echo off\n")
	new_file.write("pip install selenium\n")
	new_file.write("python install.py %s\n" % link)
	new_file.write("pause\n")
	#new_file.write("start C:\\Users\\cit-labs\\Downloads\\Dropbox 2.6.7.exe\n")
	print "[MAIN] Made file account%i.bat" % no

if __name__ == "__main__":
	assert len(sys.argv) == 4, ("Missing argument, expected 3 but got %i \n\n     python main.py [username] [password] [Number of Fakes]\n" % (len(sys.argv)-1))  

	print "[MAIN] Starting..."
	print "[MAIN] Creating %s emails for " % sys.argv[3]
	print "[MAIN] Initializing EmailManager..."
	email_manager = EmailManager()
	email_manager.create_accounts(int(sys.argv[3]))

	print "[MAIN] Filling Dropbox fields"
	driver = webdriver.Chrome()
	driver.get("https://www.dropbox.com/referrals")
	driver.find_element_by_name("login_email").send_keys(sys.argv[1])
	driver.find_element_by_id("login_password").send_keys(sys.argv[2])
	driver.find_element_by_id("login_submit").click()
	for i in email_manager.get_account_list():
		driver.find_element_by_id("referrals-page-new-collab-input").send_keys(i.get_email_address())
		driver.find_element_by_id("referrals-page-new-collab-input").send_keys(Keys.RETURN)
	driver.find_element_by_id("retrieve-contacts-button").click()

	print "\n<<<Reference Links>>>"
	j = 1
	for i in email_manager.get_emails():
		make_batch_script(j,get_email_from_body(i))
		j = j + 1
	time.sleep(3)
	print "\n[MAIN] Killing everything"
	driver.close()
	email_manager.killall()
	time.sleep(1)
	print "[MAIN] Done.\n"
