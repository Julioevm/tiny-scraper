# Tiny Scraper

![Platform](https://img.shields.io/badge/platform-Anbernic-orange.svg)

A small utility to scrape game covers for your RGXX devices

## Features

- **Easy Downloads:** Download cover media directly onto your Anbernic device.
- **User-Friendly Interface:** Simple and intuitive interface designed specifically for Anbernic devices.
- **Wide Compatibility:** Supports various ROM file types and multiple Anbernic models.

## Supported Devices

I've personally only tested it on the RG35xx H

However, it could be compatible with any Anbernic handheld with a Python version >= 3.7. Please, open an issue to confirm the compatibility or to report any problems.

## Installation

To install Tiny Scraper on your Anbernic device, follow these steps:

1. **Download the Latest Release:**
   - Navigate to the [Releases](https://github.com/Julioevm/tiny-scraper/releases) page and download the latest version of TinyScraper.zip.

2. **Transfer to Device:**
   - Extract and copy the content of the downloaded zip to the `APPS` directory of your Anbernic. You can copy it in `/mnt/sdcard/Roms/APPS` if you want the app on the SD2 or `/mnt/mmc/Roms/APPS` for the SD1.

3. **Setup config**
   - create a `config.json` file inside the `tiny_scraper` folder with a valid user and password from https://www.screenscraper.fr. Register if you haven't.
```
{
    "user": "your_user",
    "password": "your_password"
}
```
3. **Start Tiny Scraper:**
   - From the main menu, go to App Center, select Apps and launch Tiny Scraper.


## Troubleshooting

Any issue should be logged in the log.txt file inside the `tiny_scraper` folder. Open an issue and share its contents for help!