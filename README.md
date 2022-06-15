# Linkedin Scraper Selenium

Scrape LInkedin Public profile without using Linkedin API 

## What It can Do

- Scrape Public profile 
    - Name
    - Company
    - Email
    -linkedin id

## Install Requirements

Please make sure chrome is installed and ```chromedriver``` is placed in the same directory as the file

Find out which version of ```chromedriver``` you need to download in this link [Chrome Web Driver](http://chromedriver.chromium.org/downloads).

Place your Linkedin login in info into ```linkedin_credentials.txt```




```sh
pip install -r requirements.txt
```

## Usage

#### 1. Use scraper.py to print to screen or to file

```
usage: scraper.py [-h] -page PAGE -len LEN 
```

## Usage (post_scraper)
#### Use post_scraper.py for scrape profile from csv file

```
usage: post_scraper.py [-h] -fileName FILENAME
example:
post_scraper.py -f 16_12.csv
```