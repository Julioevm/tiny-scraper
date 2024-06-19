# Tiny Scraper

A small utility to scrape games for your RGXX devices

The idea is that this will be run as a RGXX app, and will crape your systems to add missing basic screenshots.

You will need a screenscraper.fr account.

## Setup

create a `config.json` file with the following content.

```
{
    "user": "your_user",
    "password": "your_password"
}
```


## TODOs

- Create .sh files to run from the device
- Investigate compatibility approach for the device (use Python 2.8 or bundle python 3.8)
- Interactive menu to select systems from a list
