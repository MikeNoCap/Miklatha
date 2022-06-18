$client = New-Object System.Net.Sockets.TCPClient("10.10.10.10", 80);
$stream = $client.GetStream(); [byte[]]$bytes = 0..65535 | ForEach-Object { 0 };
while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
    
    $sendback = "Hello World!"; 
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback);
    $stream.Write($sendbyte, 0, $sendbyte.Length);
    $stream.Flush();
}; 
$client.Close()