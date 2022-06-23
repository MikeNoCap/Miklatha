$daip = "localhost";
$daport = 87;
$enc = [Text.Encoding]::UTF8
Add-Type -AssemblyName System.Windows.Forms

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
    
    $stream = $client.GetStream(); [byte[]]$bytes = 0..65535 | ForEach-Object { 0 };
    
    try {
        while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
            $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
            $json_data = $data | ConvertFrom-Json;
            $move = 1;
            if ($json_data.device -eq "MOUSE") {
                if ($json_data.move -eq "UP") {
                    $POSITION = [Windows.Forms.Cursor]::Position;
                    $POSITION.y -= $move;
                    [Windows.Forms.Cursor]::Position = $POSITION;
                }
                if ($json_data.move -eq "RIGHT") {
                    $POSITION = [Windows.Forms.Cursor]::Position;
                    $POSITION.x += $move;
                    [Windows.Forms.Cursor]::Position = $POSITION;
                }
                if ($json_data.move -eq "DOWN") {
                    $POSITION = [Windows.Forms.Cursor]::Position;
                    $POSITION.y += $move;
                    [Windows.Forms.Cursor]::Position = $POSITION;
                }
                if ($json_data.move -eq "LEFT") {
                    $POSITION = [Windows.Forms.Cursor]::Position;
                    $POSITION.x -= $move;
                    [Windows.Forms.Cursor]::Position = $POSITION;
                }
            }
            $bytesend = $enc.GetBytes("OK");
            $stream.Write($bytesend, 0, $bytesend.Length);
            $stream.Flush();
        
        };
    }
    catch {
        continue;
    }
    $client.Close();
        
}
