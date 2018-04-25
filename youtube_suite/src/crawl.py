#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from collections import defaultdict
import pymongo


client = pymongo.MongoClient()
db = client.youtube


def pull_transcript(youtube_watch_link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # browser = webdriver.Chrome("/mnt/c/Users/Jonathan Spivack/Downloads/chromedriver_win32/chromedriver.exe", chrome_options=options)
    # browser = webdriver.Chrome("/mnt/c/Users/Jonathan Spivack/Downloads/chromedriver_win32/chromedriver.exe")
    # browser.get('https://www.youtube.com/watch?v=NAp-BIXzpGA')
    browser = webdriver.Chrome("/mnt/c/Users/ivy1g/AppData/Local/Programs/Python/Python36-32/chromedriver.exe" , chrome_options=options)

    browser.get('{}'.format(youtube_watch_link))


    try:
       element = WebDriverWait(browser, 20).until(
           EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='More actions']")))
       element.click()
    except:
       print ("Not aria-label=more actions.. trying aria-label=action menu")
       try:
           element = WebDriverWait(browser, 20).until(
               EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Action menu.']")))
           element.click()
       except Exception as e:
           print ("Nooooo whats wrong")
           print (e)
    try:
       elemz = browser.find_element_by_xpath("//yt-formatted-string[@class='style-scope ytd-menu-service-item-renderer']")
       elemz.click()

    except Exception as e:
       print ("I think there are no captions/transcript available.....")
       print (e)



    time.sleep(5)
    try:

        htmlSource = browser.page_source
        soup = BeautifulSoup(htmlSource)
        parents = soup.findAll("div",{"class":"cue-group style-scope ytd-transcript-body-renderer"})
        records = []
        captions_dict = defaultdict(list)

        for parent in parents:
            time_stamp = parent.text.strip()[0:5]
            caption = parent.text.strip()[5:]
            records.append((time_stamp.strip(), caption.strip()))

            words = caption.strip().split()

            for word in words:
                word=word.replace(".", "")
                word=word.replace("(", "")
                word=word.replace(")", "")
                word=word.replace(",", "")
                word=word.replace("!", "")
                captions_dict[word.lower()].append(time_stamp)



        df = pd.DataFrame(records, columns=['time_stamp', 'caption'])
        df.to_csv('youtube_captions.csv', index=False, encoding='utf-8')

        lastrowtime=df['time_stamp'].iloc[-1]
        print(lastrowtime)
        new_cache = {
            "url": youtube_watch_link,
            "lasttimestamp": lastrowtime,
            "captionsd": dict(captions_dict)
        }
        db.cached.insert(new_cache, check_keys=False)
    except Exception as e:
        browser.quit()
        print('lololol')
        lastrowtime=""
        normaldict={}
        

        with open('cap_dictionary.py', 'w') as medict:
            medict.write("#!/usr/bin/env python3\n\n")
            medict.write("lasttimestamp=\"{}\"\n\n".format(lastrowtime))
            medict.write("captionsd={}\n\n".format(normaldict))




    # print("appending to cache")
    # cache.append(new_cache)
    #print(cache)

    print('appending okaaaaay to db')





    ## Writing dictionary to a separate python file
    normaldict=dict(captions_dict)
    with open('cap_dictionary.py', 'w') as medict:
        medict.write("#!/usr/bin/env python3\n\n")
        medict.write("lasttimestamp=\"{}\"\n\n".format(lastrowtime))
        medict.write("captionsd={}\n\n".format(normaldict))


if __name__ == "__main__":
    pull_transcript("https://www.youtube.com/watch?v=NAp-BIXzpGA")
