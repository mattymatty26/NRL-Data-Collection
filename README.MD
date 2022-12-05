## NRL Webscraping Script

The scrape_scastats.py file is a selenium based python bot that will scrape all NRL player information from 2009 from this website https://www.nrlsupercoachstats.com/combinedstats.php and turn it into a CSV or pickle file.

If you prefer a CSV file, comment out line 100 and uncomment line 103.

This bot requires Chrome to be installed on your machine and a Chrome driver which can be installed based on your version of chrome from here https://chromedriver.chromium.org/downloads. You can set the path of the installation in a .env file under the variable path at the base of this folder location.

