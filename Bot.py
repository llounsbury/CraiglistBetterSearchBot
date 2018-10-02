from selenium import webdriver
from time import sleep

slowSystemWait = 1
captchaWait = 3

CRAIGSLISTPAGE = "https://iowacity.craigslist.org/search/mcy?postedToday=1&search_distance=2000&postal=52245"
searchList = ["125","250","450","KLR"]
avoidList = ["harley","ninja", "moped"]


#TODO: implement these
atLeastYear = 1995
avoidNoPrice = True
avoidOneDollar = True


class WebStuff:
    webDriver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
    oldProductList = []
    searchList = ["125","250","450","KLR"]
    avoidList = ["harley","ninja", "moped"]
    #TODO: Implement newer than
    atLeastYear = 1995
    #Things to look for on the page
    xPaths = [".//*[contains(@id,'titletextonly')]", ".//*[@class='mapAndAttrs']/p[1]/span/b", ".//*[contains(@class,'price')]"]
    xPathsTitles = ["Title", "Item", "Price"]

    @staticmethod
    def getPageResults():
        #generate the list of postings
        try:
            WebStuff.webDriver.get(CRAIGSLISTPAGE)
            newProductList = []
            currentProductListWebElements = (WebStuff.webDriver.find_elements_by_xpath(".//*[contains(@class,'result-title hdrlnk')]"))
            for item in currentProductListWebElements:
                currentName = (item.get_attribute("text"))
                if not WebStuff.oldProductList.__contains__(currentName) and not newProductList.__contains__(currentName):
                    x = 0
                    #TODO: Ignore price and year if included in title when looking for searchkeys
                    for searchKeys in WebStuff.searchList:
                        if searchKeys.lower() in currentName.lower() and x == 0:
                            avoid = 0
                            for avoidKey in WebStuff.avoidList:
                                if avoidKey.lower() in currentName.lower():
                                  avoid = 1
                            if avoid == 0:
                                newProductList.append(currentName)
                            #print(currentName + " has been added to newProductList")
                            x = 1
            WebStuff.getMoreInfo(newProductList)
            WebStuff.oldProductList = newProductList
            return 1
        except:
            return 0


    @staticmethod
    def getMoreInfo(productList):
        for item in productList:
            complete = 0
            while complete == 0:
                moreInfo = []
                try:
                    WebStuff.webDriver.get(CRAIGSLISTPAGE)
                    WebStuff.webDriver.find_element_by_link_text(item).click()
                    sleep(slowSystemWait)
                    moreInfo.append(WebStuff.webDriver.current_url)
                    for x in range(0, len(WebStuff.xPaths)):
                        if WebStuff.checkForXpath(WebStuff.xPaths[x]):
                            info = WebStuff.webDriver.find_element_by_xpath(WebStuff.xPaths[x])
                            moreInfo.append(info.text)
                        else:
                            moreInfo.append("Unlisted")
                    #Uncomment line below to fetch data in captcha tab
                    #moreInfo = WebStuff.getInfoInCaptcaTab(moreInfo)
                    WebStuff.notifyUser(moreInfo)
                    complete = 1
                except:
                    print("failure to get item info. Retrying")

    @staticmethod
    def getInfoInCaptcaTab(moreInfo):
        suspectedError = True
        try:
            WebStuff.webDriver.find_element_by_xpath(".//*[contains(@class,'reply_button js-only')]").click()
            sleep(captchaWait)
            contact = WebStuff.webDriver.find_element_by_xpath(".//*[@class='reply-flap js-captcha']/ul/li/h1").text
            if "contact" in contact:
                moreInfo.append(WebStuff.webDriver.find_element_by_xpath(
                    ".//*[@class='reply-flap js-captcha']/ul/li/p").text)
            else:
                moreInfo.append("Unlisted")
        except:
            moreInfo.append("Unlisted")
        try:
            moreInfo.append(
                WebStuff.webDriver.find_element_by_xpath(".//*[contains(@class,'reply-tel-number')]").text)
            suspectedError = False
        except:
            moreInfo.append("Unlisted")
        try:
            moreInfo.append(WebStuff.webDriver.find_element_by_xpath(".//*[contains(@class,'anonemail')]").text)
            suspectedError = False
        except:
            moreInfo.append("Unlisted")
        if suspectedError:
            moreInfo.append("Error in fetching Captcha tab")
        return moreInfo



    @staticmethod
    def notifyUser(moreInfo):
        notifyUser = True
        print(" ")
        for item in  moreInfo:
            print(item)
        #look at price to determine if meets input statements
        if moreInfo[3] == "Unlisted" and avoidNoPrice:
            notifyUser = False
        if moreInfo[3] == 1 and avoidOneDollar:
            notifyUser = False
        #Attempt to figure out the year


        if notifyUser:
            print("Would Notify User")
        else:
            print("Would Not Notify User")



    @staticmethod
    def checkForXpath(xPath):
        try:
            test = WebStuff.webDriver.find_element_by_xpath(xPath).__getattribute__("text")
        except:
            return False
        return True




sucsess = 0
attempt = 0
while sucsess == 0:
    sucsess = WebStuff.getPageResults()
    if sucsess ==0:
        attempt = attempt +1
        print("Attempt " + str(attempt) + " Failed. Retrying.. ")
WebStuff.webDriver.close()