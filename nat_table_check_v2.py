#!/usr/bin/python

####
# This script uses selenium to connect to an ARRIS BGW320-505
# residential gateway (used by AT&T Fiber) to check the current
# number of NAT sessions and clear the table if it exceeds a specified
# limit. Why? Because AT&T has a poorly designed setup that eventually
# causes the NAT table on their gateway to fill up, which causes
# connectivity issues. Run this script on a schedule of your choosing. 
####

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common import keys
import sched, time
import os

# Define some variables
rg_ip = '192.168.1.254' # Residential gateway management IP address
rg_password = 'YOUR_RG_PASSWORD' # password needed to login to RG
max_sessions = 1500 # Maximum sessions permitted before a reset/clear is triggered

#### 
# This section is related to K8S configuration variables
# Remark these lines out if you are not utilizing K8S and
# uncomment the variables above
###  
#rg_password = os.environ['rg_password'] # Replaces the original rg_password when running in K8S (secrets used instead)
#rg_ip = os.environ['rg_address'] # Replaces the original rg_ip when running in K8S (Configmap used instead)
#max_sessions_str = os.environ['max_sessions'] # Replaces the original max_sessions when running in K8S (Configmap used instead)
#max_sessions = int(max_sessions_str)
#### End K8S section


options = Options()
options.headless = True


def sessions_check(browser):
    try:
        row = browser.find_elements_by_xpath("//*[@class= 'table60']/tbody/tr[2]/td")
        for i in row:
            session_count = int(i.text)
        if session_count > max_sessions:
            print("Too many sessions (%s), clearing NAT table... " % session_count)
            browser.find_element_by_name('Reset').click()
        else:
            print("Session count (%s) is below configured threshold (%s), not resetting!" % (session_count, max_sessions))
    except:
        print("NAT session count not found (page load may have been delayed)... retrying")
        time.sleep(10)
        sessions_check(browser)
    
def main():
    print("===== Run Starting =====")
    browser = webdriver.Firefox(options=options, service_log_path='/dev/null')
    browser.get('http://' + rg_ip + '/cgi-bin/nattable.ha')
    if browser.title == "Login":
        print("Logging in...")
        # Need to refresh the browser, because the interface returns
        # an error regarding cookies on first load (probably a bug).
        browser.refresh()
        password = browser.find_element_by_id('password')
        password.send_keys(rg_password)
        browser.find_element_by_name('Continue').click()
        sessions_check(browser)
    elif browser.title == "NAT Table":
        print("Already logged in...")
        sessions_check(browser)
    else:
        print("Something went wrong and this script is unable to continue!")
    #s.enter(60 * check_min, 1, main, (sc,))
    browser.quit()
    print("===== Run Completed =====")

main()