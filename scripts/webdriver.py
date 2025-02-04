from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import sys
import time
import traceback

# Parsers
import nbadriver
import nfldriver
import nhldriver


class Dispatch(object):
    def parse_nfl(self, html):
        nfldriver.parse(html)

    def parse_nba(self, html):
        nbadriver.parse(html)

    def parse_nhl(self, html):
        nhldriver.parse(html)

    def __getitem__(self, name):
        return getattr(self, name)


def run_driver(run_jobs):
    dispatch = Dispatch()
    while True:
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(chrome_options=chrome_options)
        
        try:
            for job in run_jobs:
                driver.get(job["url"])
                time.sleep(10)
                html = driver.page_source
                print("parsing {}...".format(job["name"]))
                action = job["action"]
                dispatch[action](html)
        except:
            driver.close()
            driver.quit()

        driver.close()
        driver.quit()


if __name__ == "__main__":
    try:
        # Ensure timezone is consistent
        os.environ["TZ"] = "America/New_York"
        
        run_jobs = [
            {
                "url": "https://www.espn.com/nba/scoreboard",
                "name": "NBA",
                "action": "parse_nba",
            },
            {
                "url": "https://www.espn.com/nfl/scoreboard",
                "name": "NFL",
                "action": "parse_nfl",
            },
            {
                "url": "https://www.espn.com/nhl/scoreboard",
                "name": "NHL",
                "action": "parse_nhl",
            },
        ]

        job = [
            {
                "url": "https://www.espn.com/nhl/scoreboard",
                "name": "NHL",
                "action": "parse_nhl",
            }
        ]

        run_driver(run_jobs)
    except Exception:
        traceback.print_exc()
        print("exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

