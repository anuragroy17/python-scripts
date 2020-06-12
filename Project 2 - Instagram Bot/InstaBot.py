from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep, strftime
import getpass
from random import randrange


class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/")
        sleep(2)

        emailInput = bot.find_elements_by_css_selector('form input')[0]
        passwordInput = bot.find_elements_by_css_selector('form input')[1]
        emailInput.clear()
        passwordInput.clear()
        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        btnLogin = bot.find_element_by_xpath('//button[@type="submit"]')
        btnLogin.click()
        sleep(5)

        notnow = bot.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]")
        notnow.click()
        sleep(3)

        notnow = bot.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]")
        notnow.click()

    def multifollow(self, accountName):
        bot = self.bot

        count = self._loadList(accountName)
        list = self._scrollList(count)

        for user in list.find_elements_by_css_selector('li'):
            userBtn = user.find_element_by_css_selector('button')
            if userBtn.text == "Follow":
                userBtn.click()
                sleep(randrange(4) + 1)
            elif userBtn.text == "Following":
                userBtn.click()
                sleep(1)
                bot.find_element_by_css_selector(
                    "button.aOOlW:nth-child(1)").click()
                sleep(randrange(4) + 1)
            elif userBtn.text == "Requested":
                userBtn.click()
                sleep(1)
                bot.find_element_by_css_selector(
                    "button.aOOlW:nth-child(1)").click()
                sleep(randrange(4) + 1)

        self._closeList()

    def getFollowerList(self, accountName):
        count = self._loadList(accountName)
        list = self._scrollList(count)
        #  Get Data Mining of followers User Account Urls
        following = []
        for user in list.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href')
            # print(userLink)
            following.append(userLink)
            if (len(following) == count):
                break

        #  Print to an external file
        print(following)
        print(len(following))
        #  Complete Data Mining of followers User Account Urls

        self._closeList()

    def _loadList(self, accountName):
        bot = self.bot

        bot.get(f"https://www.instagram.com/{accountName}/")
        sleep(3)

        following_button = bot.find_element_by_xpath(
            "//a[contains(@href,'/following')]/span")
        following_button.click()
        count = int(following_button.text)
        # print(count)

        sleep(3)
        return count

    def _scrollList(self, count):
        bot = self.bot

        list = bot.find_element_by_xpath("//div[@role='dialog']")
        list.click()

        links = list.find_elements_by_xpath("//li")
        loaded_names_count = len(links)

        actionChain = webdriver.ActionChains(bot)
        while (loaded_names_count < count):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            sleep(randrange(2) + 1)
            links = list.find_elements_by_xpath("//li")
            loaded_names_count = len(links)

        sleep(4)
        return list

    def _closeList(self):
        bot = self.bot
        closeBtn = bot.find_element_by_css_selector('[aria-label=Close]')
        closeBtn.click()

    def logout(self):
        bot = self.bot

        bot.get(f'https://www.instagram.com/{self.username}/')
        sleep(3)

        settings = bot.find_element_by_css_selector('[aria-label=Options]')
        settings.click()
        sleep(2)

        logOut = bot.find_element_by_xpath(
            "//button[contains(text(), 'Log Out')]")
        logOut.click()
        sleep(2)

    def closeBrowser(self):
        self.bot.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


try:
    username = input("Username: ")
    password = getpass.getpass()
    accountId = input("Account ID/Username to crawl: ")
    choice = int(
        input(f"Enter 1 for Multifollow (Use with Caution) or 2 for getting Followers URL List of '{accountId}'"))

    print("Automating your insta life...wait!!")
    botCrawl = InstaBot(username, password)
    botCrawl.login()

    if(choice == 1):
        botCrawl.multifollow(accountId)
    elif(choice == 2):
        botCrawl.getFollowerList(accountId)
    else:
        botCrawl.logout()
        botCrawl.closeBrowser()
        raise ValueError("Please select 1 or 2")

    botCrawl.logout()
    botCrawl.closeBrowser()

except Exception as error:
    print('ERROR', error)
