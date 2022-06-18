$wshell = New-Object -ComObject wscript.shell;
$wshell.AppActivate("Notepad");
$wshell.SendKeys('a')