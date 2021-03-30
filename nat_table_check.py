#!/usr/bin/python

####
# This script uses splinter/selenium to connect to an ARRIS NVG599
# residential gateway (used by AT&T Fiber) to check the current
# number of NAT sessions and clear the table if it exceeds a specified
# limit. Why? Because AT&T has a poorly designed setup that eventually
# causes the NAT table on their gateway to fill up, which causes
# connectivity issues. Run this script on a schedule of your choosing. 
####

from splinter import Browser
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

#s = sched.scheduler(time.time, time.sleep)

def sessions_check(browser):
    try:
        sessions = browser.find_by_tag('td')[1]
        session_count = int(sessions.text)
        if session_count > max_sessions:
            print("Too many sessions (%s), clearing NAT table... " % session_count)
            browser.find_by_name('Reset').click()
        else:
            print("Session count (%s) is below configured threshold (%s), not resetting!" % (session_count, max_sessions))
    except:
        print("NAT session count not found (page load may have been delayed)... retrying")
        sessions_check(browser)

def main():
    print("===== Run Starting =====")
    browser = Browser('firefox', headless=True)
    browser.visit('http://' + rg_ip + '/cgi-bin/nattable.ha')
    if browser.is_text_present('Device Access Code'):
        print("Logging in...")
        browser.fill('password', rg_password)
        browser.find_by_name('Continue').click()
        sessions_check(browser)
    elif browser.is_text_present('Total sessions in use'):
        print("Already logged in...")
        sessions_check(browser)
    else:
        print("Something went wrong and this script is unable to continue!")
    #s.enter(60 * check_min, 1, main, (sc,))
    browser.quit()
    print("===== Run Completed =====")

#s.enter(60 * check_min, 1, main, (s,))
#s.run()
main()