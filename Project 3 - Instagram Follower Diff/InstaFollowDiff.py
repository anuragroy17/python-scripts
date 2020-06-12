from selenium import webdriver
from time import sleep, strftime
import getpass


class InstaFollowDiff:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("https://www.instagram.com/")
        sleep(2)

        # loginBtn = bot.find_element_by_xpath("//a[contains(text(), 'Log in')]")
        # loginBtn.click()
        # sleep(1)

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

    def logout(self):
        bot = self.bot

        if bot.current_url != f'https://www.instagram.com/{self.username}':
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

    def closeBrowser(self):
        self.bot.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


try:
    username = input("Username: ")
    password = getpass.getpass()

    print("Automating your insta life...wait!!")
    botCrawl = InstaFollowDiff(username, password)
    botCrawl.login()

    botCrawl.logout()
    botCrawl.closeBrowser()

except Exception as error:
    print('ERROR', error)
