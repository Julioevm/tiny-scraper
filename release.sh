# This script will bundle the necessary files for a release and create a zip file

ZIP_FILE="tiny-scraper.zip"

# Remove the existing zip file if it exists
if [ -f "$ZIP_FILE" ]; then
    rm "$ZIP_FILE"
fi

# Create the zip file with the necessary files and directories
zip -r "$ZIP_FILE" tiny-scraper.sh tiny_scraper Imgs README.md

echo "Release bundle created: $ZIP_FILE"