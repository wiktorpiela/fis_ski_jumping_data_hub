import pandas as pd
from urllib import request
import re, os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def open_and_get_pdf_link(href):
    
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(str(href))
        driver.find_element_by_xpath("//*[contains(text(),'Official Results')]").click()
        driver.switch_to.window(driver.window_handles[1])
        cur_link = driver.current_url
        driver.close()
        driver.quit()
        
        return cur_link
        
    except NoSuchElementException:
        
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(str(href))
        driver.find_element_by_xpath("//*[contains(text(),'Results 1st Round')]").click()
        driver.switch_to.window(driver.window_handles[1])
        cur_link1 = driver.current_url
        driver.close()
        driver.quit()
        
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(str(href))
        driver.find_element_by_xpath("//*[contains(text(),'Result 2nd Round')]").click()
        driver.switch_to.window(driver.window_handles[1])
        cur_link2 = driver.current_url
        driver.close()
        driver.quit()
        
        return [cur_link1, cur_link2]



# zawody indywidualne na normlanych, duych skoczniach i loty, mezczyzni, 2009-2022
# scprapowanie linków do kazdego eventu

events_per_season = []

for x in range(2009,2023):
    html = request.urlopen("https://www.fis-ski.com/DB/general/statistics.html?statistictype=positions&positionstype=position&offset=50&sectorcode=JP&seasoncode="+str(x)+"&categorycode=WC&gendercode=M&competitornationcode=&place=&nationcode=&position=4&disciplinecode=NH,LH,FH")
    text = html.read()
    plaintext = text.decode('utf8')
    links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
    links = pd.DataFrame(links).rename(columns={0:"hrefs"})
    events_per_season.append(links[links["hrefs"].str.contains("raceid=",regex=False)].drop_duplicates()["hrefs"])
   
events_per_season = events_per_season = pd.concat(events_per_season,ignore_index=True).to_list()


# scrapowanie linków do PDF z wynikami kazdego eventu (official results)

pdfs = []

for x in events_per_season:
    
    print(x)
    pdfs.append(open_and_get_pdf_link(x+"#down"))


# pobranie tych pdf


for x in range(len(pdfs)):
    
    if type(pdfs[x]) is str:
        remote_url = pdfs[x]
        local_file = os.getcwd()+"//pdfs//"+str(x)+".pdf"
        request.urlretrieve(remote_url, local_file)
      
    else:
        
        for y in range(len(pdfs[x])):
            remote_url = pdfs[x][y]
            local_file = os.getcwd()+"//pdfs//"+str(x)+"_"+str(y)+".pdf"
            request.urlretrieve(remote_url, local_file)