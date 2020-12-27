from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import getpass
from random import randrange
import csv


class UserDetails:
    def __init__(self):
        self.bot = webdriver.Firefox()
        self.count = 0

    def login(self, username, password):
        self.count += 1
        bot = self.bot

        if self.count == 1:
            bot.get("https://www.instagram.com/")

        sleep(2)

        emailInput = bot.find_elements_by_css_selector('form input')[0]
        passwordInput = bot.find_elements_by_css_selector('form input')[1]
        emailInput.clear()
        passwordInput.clear()

        emailInput.send_keys(username)
        passwordInput.send_keys(password)
        btnLogin = bot.find_element_by_xpath('//button[@type="submit"]')
        btnLogin.click()
        sleep(5)

        notnow = bot.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]")
        notnow.click()
        sleep(3)

        try:
            notnow = bot.find_element_by_xpath(
                "//button[contains(text(), 'Not Now')]")
            notnow.click()

        except:
            print("Not Now button skipped")

    def openUser(self, username):
        bot = self.bot

        profile = bot.find_element_by_xpath(
            "//a[contains(@href,'/{}')]".format(username))
        profile.click()
        sleep(2)

    def getFollowing(self):
        bot = self.bot

        following_button = bot.find_element_by_xpath(
            "//a[contains(@href,'/following')]/span")
        following_button.click()
        following = self._get_names(int(following_button.text))
        # print("following-"+str(len(following)))
        return following

    def _get_names(self, count):
        sleep(3)
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

        names = []
        for user in list.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href')
            # print(userLink)
            names.append(userLink)
            if (len(names) == count):
                break

        # close button
        closeBtn = bot.find_element_by_css_selector('[aria-label=Close]')
        closeBtn.click()
        return names

    def logout(self, username):
        bot = self.bot
        if bot.current_url != f'https://www.instagram.com/{username}/':
            profile = bot.find_element_by_xpath(
                "//a[contains(@href,'/{}')]".format(username))
            profile.click()
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


class FinalDetails:
    def __init__(self, following1, following2):
        self.following1 = following1
        self.following2 = following2

    def getCommonAccounts(self):
        commons = [
            user for user in self.following1 if user in self.following2]

        with open('common-users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Url"])
            for x in commons:
                writer.writerow([x[26:len(x)-1], x])

        print("Please find common-users.csv file for common users")


try:
    print("Enter the Instagram Accounts to Compare")
    username1 = input("Username of Account 1: ")
    password1 = getpass.getpass()

    username2 = input("Username of Account 2: ")
    password2 = getpass.getpass()

    print("Automating your insta life...wait!!")
    botCrawl = UserDetails()
    botCrawl.login(username1, password1)
    botCrawl.openUser(username1)
    following1 = botCrawl.getFollowing()
    botCrawl.logout(username1)

    botCrawl.login(username2, password2)
    botCrawl.openUser(username2)
    following2 = botCrawl.getFollowing()
    botCrawl.logout(username2)

    botCrawl.closeBrowser()

    computeUsers = FinalDetails(following1, following2)
    computeUsers.getCommonAccounts()


except Exception as error:
    print('ERROR', error)
