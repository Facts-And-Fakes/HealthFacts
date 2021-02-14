#importing all the necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import randomAgent

#defining the googleSearch function
def googleSearch(query):
    #making the url ready for requests
    url = 'https://www.google.com/search?q=site%3Aun.org+{}'.format(query);
    user_agent = randomAgent.getUA()
    ran_head = {
            'user-agent': user_agent,
        }
    g_clean=[]
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if(re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            return [g_clean[0],g_clean[1],g_clean[2],g_clean[3],g_clean[4]]
        except:
            return ['https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/water/art-20044256', 'https://www.healthline.com/nutrition/how-much-water-should-you-drink-per-day', 'https://www.healthline.com/health/how-much-water-should-I-drink', '', '']
