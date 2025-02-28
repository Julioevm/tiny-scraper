# Tiny Scraper

![Platform](https://img.shields.io/badge/platform-Anbernic-orange.svg)

A small utility to scrape game covers for your RGXX devices

## Features

- **Easy Downloads:** Download cover media directly onto your Anbernic device.
- **User-Friendly Interface:** Simple and intuitive interface designed specifically for Anbernic devices.
- **Wide Compatibility:** Supports various ROM file types and multiple Anbernic models.

## Supported Devices

I've personally only tested it on the RG35XX H
RG40XXV, RGcubeXX and RG28xx should be supported.

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
    "password": "your_password",
    "media_type": "sstitle",
    "region": "wor",
    "resize": false
}
```

- Media type let's you select the type of media to download: The main options I suggest are `ss` for a game screenshot, `sstitle`, for the title screen or `box-2D` or `box-3D` (Keep the capital letters) for a box, `mixrbv1` or `mixrbv2` for a mix of screenshot, wheel and so on. For more options check the [screenscraper.fr documentation](https://api.screenscraper.fr/api2/jeuInfos.php?devid=xxx&devpassword=yyy&softname=zzz&output=xml&ssid=test&sspassword=test&crc=50ABC90A&systemeid=1&romtype=rom&romnom=Sonic%20The%20Hedgehog%202%20(World).zip&romtaille=749652)—search in the list for the media entries.  Note that box and mix might be of bigger size than `ss` or `sstitle` In some cases it can cause the game list to load slower.

- Region let's you prioritize the region of the media to download. Some games have different covers for Japan, some for Europe and some for the rest of the world. If the region is not specified it will prioritize the world covers, also if the media type is not available on the preferred region, we will get the first one available. Valid regions are `wor`, `jp`, `eu`, `asi`, `kr`, `ss`, `us`.

- Resize: `true` or `false` — Will resize the downloaded media to 320 by 240, saving space and avoiding slowdowns when listing the roms. But it might make scraping in bulk a bit slower.

3. **Start Tiny Scraper:**
   - From the main menu, go to App Center, select Apps and launch Tiny Scraper.


## Troubleshooting

Old version of stock OS might cause issues. V 1.0.3 (20240511) hs been reported to miss some necessary libraries: No module named 'PIL' try to update in this case.

Any issue should be logged in the log.txt file inside the `tiny_scraper` folder. Open an issue and share its contents for help!
