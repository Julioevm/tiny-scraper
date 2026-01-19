$ZIP_FILE = "tiny-scraper.zip"

if (Test-Path $ZIP_FILE) {
    Remove-Item -Path $ZIP_FILE -Force
}

Compress-Archive -Path "tiny-scraper.sh", "tiny_scraper", "Imgs", "README.md" -DestinationPath $ZIP_FILE

Write-Host "Release bundle created: $ZIP_FILE"
