import json
import time
from selenium import webdriver
from subprocess import Popen, PIPE


nordvpn_path = "C:\\Program Files\\NordVPN\\nordvpn.exe"
nord_countries_path = "nord_countries.json"


def connect(country: str):
    print("Connecting to " + country)

    proc = Popen([nordvpn_path, "-c", "-g", country], stdin=PIPE,
                 universal_newlines=True, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()

    time.sleep(10)

    print(out, err)
    print("Connected to " + country)


def disconnect():
    print("Disconnecting...")

    proc = Popen([nordvpn_path, "--disconnect"], stdin=PIPE,
                 universal_newlines=True, stdout=PIPE, stderr=PIPE)

    out, err = proc.communicate()

    time.sleep(10)

    print(out, err)
    print("Disconnected")


def scrape(country: str):

    connect(country=country)

    wd = webdriver.Chrome()
    wd.get("https://www.netflix.com/signup/planform")

    res = wd.execute_script("return netflix.reactContext")
    options = res["models"]["flow"]["data"]["fields"]["planChoice"]["options"]

    for option in options:
        price = option["fields"]["planPriceAmount"]["value"]
        currency = option["fields"]["planPriceCurrency"]["value"]
        print(country + " " + price + " " + currency)

    wd.quit()

    disconnect()

    return {
        "country": country,
        "options": options
    }


def main():
    countries = []
    options = []

    with open(nord_countries_path) as f:
        countries = json.load(f)

    for country in countries:
        try:
            res = scrape(country=country)
            if res:
                options.append(res)
        except:
            print("Error while scraping")

    options_json = json.dumps(options, indent=4)

    with open("result.json", "w") as outfile:
        outfile.write(options_json)


if __name__ == "__main__":
    main()
