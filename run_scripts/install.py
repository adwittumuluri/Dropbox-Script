import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def make_account(link,driver):
	driver.get(link)
	driver.find_element_by_id("fname").send_keys("John")
	driver.find_element_by_id("lname").send_keys("Doe")
	uname = driver.find_element_by_id("email").get_attribute("value")
	driver.find_element_by_id("password").send_keys("[YOUR PASSWORD]")
	driver.find_element_by_id("tos_agree").click()
	driver.find_element_by_id("register-submit").click()


	print "Done."
	print "\n\nUsername: %s" % uname
	print "Password: [YOUR PASSWORD]\n"

if __name__ == "__main__":
	link = sys.argv[1]
	driver = webdriver.Chrome()
	make_account(link,driver)
