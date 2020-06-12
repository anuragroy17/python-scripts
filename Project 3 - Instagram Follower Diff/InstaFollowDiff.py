from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import getpass
from random import randrange
import csv


class InstaFollowDiff:
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

    def openUser(self):
        bot = self.bot

        profile = bot.find_element_by_xpath(
            "//a[contains(@href,'/{}')]".format(self.username))
        profile.click()
        sleep(2)

    def get_unfollowers(self):
        bot = self.bot

        following_button = bot.find_element_by_xpath(
            "//a[contains(@href,'/following')]/span")
        following_button.click()
        following = self._get_names(int(following_button.text))
        followers_button = bot.find_element_by_xpath(
            "//a[contains(@href,'/followers')]/span")
        followers_button.click()
        followers = self._get_names(int(followers_button.text))
        not_following_back = [
            user for user in following if user not in followers]

        with open('unfollowers.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Url"])
            for x in not_following_back:
                writer.writerow([x, f'https://www.instagram.com/{x}/'])

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

        nameList = list.find_elements_by_tag_name('a')
        names = [name.text for name in nameList if name.text != '']
        # close button
        closeBtn = bot.find_element_by_css_selector('[aria-label=Close]')
        closeBtn.click()
        return names

    def logout(self):
        bot = self.bot
        if bot.current_url != f'https://www.instagram.com/{self.username}/':
            profile = bot.find_element_by_xpath(
                "//a[contains(@href,'/{}')]".format(self.username))
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


class unfollowers:
    def __init__(self, name, url):
        self.name = name
        self.url = url


try:
    username = input("Username: ")
    password = getpass.getpass()

    print("Automating your insta life...wait!!")
    botCrawl = InstaFollowDiff(username, password)
    botCrawl.login()
    botCrawl.openUser()
    botCrawl.get_unfollowers()

    botCrawl.logout()
    botCrawl.closeBrowser()

except Exception as error:
    print('ERROR', error)
