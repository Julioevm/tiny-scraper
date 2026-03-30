$ErrorActionPreference = "Stop"
$ZIP_FILE = "tiny-scraper.zip"

if (Test-Path $ZIP_FILE) {
    Remove-Item -Path $ZIP_FILE -Force
}

$STAGING = "release-staging"
if (Test-Path $STAGING) {
    Remove-Item -Path $STAGING -Recurse -Force
}
New-Item -Path $STAGING -ItemType Directory | Out-Null

Copy-Item -Path "tiny-scraper.sh", "README.md" -Destination $STAGING
Copy-Item -Path "tiny_scraper", "Imgs" -Destination $STAGING -Recurse

$textExtensions = @("*.sh", "*.py", "*.md", "*.txt", "*.cfg", "*.ini", "*.json", "*.yaml", "*.yml", "*.toml")

Get-ChildItem -Path $STAGING -Recurse -Include $textExtensions | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    $normalized = $content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($_.FullName, $normalized)
}

Compress-Archive -Path "$STAGING\*" -DestinationPath $ZIP_FILE

Remove-Item -Path $STAGING -Recurse -Force

Write-Host "Release bundle created: $ZIP_FILE"
