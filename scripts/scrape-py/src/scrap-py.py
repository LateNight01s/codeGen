# for html scrapping
import requests
from bs4 import BeautifulSoup
# for screenshot
from selenium import webdriver
from PIL import Image
from io import BytesIO


# this functions get the links for the templated comtaining the html code and output from the w3-schools
def get_links(url):
    base_htm_code=requests.get(url)
    base_html = BeautifulSoup(base_htm_code.text,'html.parser')
    # links is the list of all the links of the webpages with html code frame and output frame of w3-schools
    links=[]

    for link in base_html.find_all("a",{"class":"w3-button w3-bar-item w3-light-grey"}):
        links.append("https://www.w3schools.com/html/"+link.get('href'))
    for link in base_html.find_all("a",{"class":"w3-button w3-bar-item w3-light-grey w3-border-top"}):
        links.append("https://www.w3schools.com/html/"+link.get('href'))

    return links


# this function decodes the html and removes the encoded symbol by there respective html symbol (specially used to remove &lt; & &gt which are < , >)
def html_decode(s):
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


# this function is used to scrap the html
def get_html(links):     #the perimeter of links is passed as it contains the list of the links of the pages from where the html code has to be extracted
    directory="A:\Workspace\html_scrapper\html_scrapped_CodeFiles"
    print("The Total number of links available are :",len(links))

    for (i,link) in enumerate(links):
        main_htm_code=requests.get(link)
        main_html = BeautifulSoup(main_htm_code.text,'html5lib')
        div=str(main_html.find("div",{"id":"textareacontainer"}))
        
        # this has some extra piece of code that is stripped below
        decoded_div=html_decode(div)

        # here the extra piece of code is being is stripped
        strip_html_fromDiv=decoded_div[decoded_div.find("<html>"):decoded_div.find("</html>")+7].strip()
        
        # print(decoded_div)
        #here we write the strip_html_fromDiv in the html file 
        with open(f"{directory}\{i}.html","w+") as fp: 
            try:
                fp.write(strip_html_fromDiv)
            except Exception as err:
                print("Exception occured @ ",i,err)
                continue


# this function automates the process taking screenshots of the links
def get_screenshots(links):
    directory="A:\Workspace\html_scrapper\html_scrapped_screenshots"
    for (i,link) in enumerate(links):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized") #forcing browser to open in maximized mode
            chrome = webdriver.Chrome(chrome_options=options)
            chrome.get(link)
            element = chrome.find_element_by_id('iframewrapper') # find part of the page you want image of
            location = element.location
            size = element.size
            png = chrome.get_screenshot_as_png( ) # saves screenshot of entire page
            chrome.quit()

            im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            im = im.crop((left, top, right, bottom)) # defines crop points
            im.save(f"{directory}\{i}.png") # saves new cropped image
        except Exception as err:
            print(err)
            exit()
    

# main function
if __name__=="__main__":
    url="https://www.w3schools.com/html/html_examples.asp"
    links=get_links(url)
    get_html(links)
    get_screenshots(links)