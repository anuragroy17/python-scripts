import psutil
import time
import pyttsx3
from win10toast import ToastNotifier
import threading

# save file with extension .pyw and save it with the icon in windows startup folder
# for win10toast to show up, press win+i>System>Notification & Actions>Switch on "Get Notications from apps and others"

toaster = ToastNotifier()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female, 0 for male
engine.setProperty('rate', 120)
engine.setProperty('volume', 8)
count = 0


def showToastrNotifications(text):
    # For same folder, use for debugging
    toaster.show_toast(text, icon_path='battery_icon.ico', duration=10)

    # Full path, use when using locally on windows
    # toaster.show_toast(text, icon_path="C://battery_icon.ico", duration=10)

    # looping the toaster for some period of time
    while toaster.notification_active():
        time.sleep(0.1)


def monitorPercentage():
    global count
    while (True):
        time.sleep(10)
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = int(battery.percent)

        if percent < 15:
            if plugged == False:
                processThread = threading.Thread(target=showToastrNotifications, args=(
                    f"Battery is at {percent}% Please plug the cable",))  # <- note extra ','
                processThread.start()
                engine.say(
                    "Your battery is getting low so plug in your charger")
                engine.runAndWait()
                count = 0
        elif percent == 100:
            if plugged == True:
                processThread = threading.Thread(target=showToastrNotifications, args=(
                    "Battery is Fully Charged",))
                processThread.start()
                engine.say(
                    "Battery is fully charged, please unplug the charger")
                engine.runAndWait()
        elif percent == 90:
            if plugged == True:
                if count == 0:
                    processThread = threading.Thread(target=showToastrNotifications, args=(
                        "Your Battery at 90%. You can unplug the charger.",))
                    processThread.start()
                    engine.say(
                        "Your battery is at 90%, you can unplug the charger")
                    engine.runAndWait()
                    count = count + 1


if __name__ == "__main__":
    monitorPercentage()
