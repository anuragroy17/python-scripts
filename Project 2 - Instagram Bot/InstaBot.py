
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep, strftime
import getpass 

# Remaining:-
# fixing sleep timers - replace with wait for element visibility
# handling errors

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/")
        sleep(3)
        
        loginBtn = bot.find_element_by_css_selector("#react-root > section > main > article > div.rgFsT > div:nth-child(2) > p > a")
        loginBtn.click()
        sleep(1)

        emailInput = bot.find_elements_by_css_selector('form input')[0]
        passwordInput = bot.find_elements_by_css_selector('form input')[1]
        emailInput.clear()
        passwordInput.clear()
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        btnLogin = bot.find_element_by_css_selector("#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4)")
        btnLogin.click()
        sleep(4)

        notnow = bot.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm")
        notnow.click()

    def multifollow(self, accountName, max):
        bot = self.bot

        bot.get(f"https://www.instagram.com/{accountName}/")
        sleep(3)

        followersBtn = bot.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(3) > a")
        followersBtn.click()
        sleep(3)

        followersList = bot.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(bot)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            sleep(2)
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        
        print(numberOfFollowersInList)

        for user in followersList.find_elements_by_css_selector('li'):
            userBtn = user.find_element_by_css_selector('button')
            if userBtn.text == "Follow":
                userBtn.click()
                sleep(3)
            elif userBtn.text == "Following":
                userBtn.click()
                sleep(1)
                bot.find_element_by_css_selector("button.aOOlW:nth-child(1)").click()
                sleep(3)

        # buttonList = bot.find_element_by_css_selector('div[role=\'dialog\'] button') #old method
        closeBtn = bot.find_element_by_css_selector('[aria-label=Close]')
        closeBtn.click()

        #  Get Data Mining of followers User Account Urls
        # followers = []
        # for user in followersList.find_elements_by_css_selector('li'):
        #     userLink = user.find_element_by_css_selector('a').get_attribute('href')
        #     # print(userLink)
        #     followers.append(userLink)
        #     if (len(followers) == max):
        #         break        
        # print(followers)

    def getFollowerList(self, accountName, max):
        bot = self.bot

        bot.get(f"https://www.instagram.com/{accountName}/")
        sleep(3)

        followersBtn = bot.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(3) > a")
        followersBtn.click()
        sleep(3)

        followersList = bot.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(bot)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            sleep(2)
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        
        # print(numberOfFollowersInList)
        
        #  Get Data Mining of followers User Account Urls
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        # print(followers)

        closeBtn = bot.find_element_by_css_selector('[aria-label=Close]')
        closeBtn.click()

    def logout(self):
        bot = self.bot

        profile = bot.find_element_by_css_selector('[aria-label=Profile]')
        profile.click()
        sleep(3)

        settings = bot.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR > div > button > span')
        settings.click()
        sleep(2)

        logOut = bot.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > button:nth-child(8)')
        logOut.click()

    def closeBrowser(self):
        self.bot.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()

try:
    username = input("Username: ")
    password = getpass.getpass()    
    accountId = input("Account ID to crawl: ")
    followerNo = input("No. of Followings of that Account: ")
    choice = int(input("Enter 1 for multifollow or 2 for getting Following URL List: "))

    print("Automating your insta life...wait!!")    
    botCrawl = InstaBot(username,password)
    botCrawl.login()

    if(choice == 1):
        botCrawl.multifollow(accountId,int(followerNo))
    elif(choice == 2):
        botCrawl.getFollowerList(accountId,int(followerNo))
    else:
        botCrawl.logout()
        botCrawl.closeBrowser()
        raise ValueError("Please select 1 or 2")


    botCrawl.logout()
    botCrawl.closeBrowser()
    
except Exception as error: 
    print('ERROR', error)

    
    