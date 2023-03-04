#Selenium imports
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#Other imports
import os                                       # For path
import sys                                      # For exit
from time import sleep                          # For sleep
from pynput import mouse
import keyboard

class App:
    nb_words = 359
    nb_secs = 60
    space_delay = 0.09

    def __init__(self):
        ## Get Chrome driver path
        cur_path = os.curdir + os.sep + "Chrome_driver" + os.sep + "chromedriver.exe"
        options = webdriver.ChromeOptions()

        ## To exclude terminal errors from chrome session
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        ## Use as extern/global variable to avoid be close at process finish
        global driver 
        
        ## Instanciate a chrome window instance
        driver = webdriver.Chrome(cur_path,options=options)
        driver.get("https://10fastfingers.com/typing-test/french")

        ## Create list
        self.list = []
        self.it = 0

        # Compute time for typing a word
        self.word_delay = (self.nb_secs-(self.nb_words*self.space_delay))/self.nb_words
        print("Number of words: "+str(self.nb_words)+"\nTime for a word: "+str(self.word_delay)+"\nRunning program...")

    def run(self):
        ## Accept cookies
        sleep(2)
        self.__accept_cookies()

        ## Collect all words
        self.__collect_words()
        sleep(0.5)

        ## Focus in input
        self.__focus_input()

        ## Type list of words
        for word in self.list:
            if(self.__check_time()):
                self.__type_word(word)
            else:
                print("Finished.")
                break

        sys.exit()

        ## Close
        #driver.close()

    def __accept_cookies(self):
        print("Accepting cookies..")
        for i in range(2,5):
            path = "/html/body/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div/div/div/fieldset/div["+str(i)+"]/div/input"
            driver.find_element_by_xpath(path).click()
            sleep(0.1)
        path_ok = "/html/body/div[1]/div/div[4]/div/div[2]/button[1]"
        driver.find_element_by_xpath(path_ok).click()
        sleep(1)

    def __focus_words(self):
        path = "/html/body/div[5]/div/div[4]/div/div[1]/div[7]/div[1]/div/span["+str(self.nb_words)+"]"
        try:
            element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, path)))
        finally:
            print("Collecting words")

    def __collect_words(self):
        # Wait words
        self.__focus_words()
        # Fill words list by getting each element text
        for i in range(self.nb_words):
            path = "/html/body/div[5]/div/div[4]/div/div[1]/div[7]/div[1]/div/span["+str(self.it+1)+"]"
            element = driver.find_element_by_xpath(path)
            self.list.append(element.get_attribute("innerText"))
            self.it += 1
        print(str(self.it)+" words collected.")

    def __focus_input(self):
        path = "/html/body/div[5]/div/div[4]/div/div[1]/div[7]/div[2]/div/div[1]/input"
        try:
            element = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, path)))
            element.click()
        finally:
            print("Start typing...")

    def __check_time(self):
        path = "/html/body/div[5]/div/div[4]/div/div[1]/div[7]/div[2]/div/div[2]/div[1]"
        element = driver.find_element_by_xpath(path)
        if(element.get_attribute("innerText")!="0:00"):
            return True
        else:
            return False


    def __type_word(self, word):
        keyboard.write(word)
        sleep(0.05)
        keyboard.send("space")
        sleep(0.05)

app = App().run()