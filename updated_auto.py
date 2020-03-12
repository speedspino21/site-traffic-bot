import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

clicks= input("Enter number of clicks: ")

proxy_list = open('proxies.txt', 'r')
proxy_list = proxy_list.read().split('\n')
proxy_list = proxy_list[:-1]
proxy_list = [x.replace('\r','') for x in proxy_list]

def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

for click_num in range(int(clicks)):
    print("Click Number: "+str(click_num)+" | Total Clicks: "+str(clicks))
    proxy = random.choice(proxy_list)
    webdriver.DesiredCapabilities.CHROME['proxy']={
                "httpProxy":proxy,
                "sslProxy":proxy,
                "proxyType":"MANUAL"
            }
    print('using proxy: '+proxy)
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = random_line('url.txt')
    print(url)
    driver.get(url)
    current_window = driver.current_window_handle
    
    timeout = random.randint(3,9)
    print("waiting for "+str(timeout)+" seconds before clicking ad.")
    time.sleep(timeout)
    
    link = driver.find_element_by_css_selector("ins[data-ad-slot='2837895721'")
    
    if not link:
        print('No google ads found on the page.')
        driver.close()
        continue
    else:
        ActionChains(driver) \
            .key_down(Keys.SHIFT) \
            .click(link) \
            .key_up(Keys.SHIFT) \
            .perform()

    new_window = [window for window in driver.window_handles if window != current_window]
    
    if(new_window):
        driver.switch_to.window(new_window[0])
    
    timeout = random.randint(6,9)
    print("waiting for "+str(timeout)+" seconds on ad page")
    time.sleep(timeout)

    driver.close()
    if(new_window):
        driver.switch_to.window(current_window)

    timeout = random.randint(1,3)
    print("waiting for "+str(timeout)+" seconds before closing the window.")
    time.sleep(timeout)
    if(new_window):
        driver.close()
