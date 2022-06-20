$Path = "C:\ScreenCapture"
# Make sure that the directory to keep screenshots has been created, otherwise create it
If (!(test-path $path)) {
    New-Item -ItemType Directory -Force -Path $path
}
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
# Get the current screen resolution
$image = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
# Create a graphic object
$graphic = [System.Drawing.Graphics]::FromImage($image)
$point = New-Object System.Drawing.Point(0, 0)
$graphic.CopyFromScreen($point, $point, $image.Size);
$cursorBounds = New-Object System.Drawing.Rectangle([System.Windows.Forms.Cursor]::Position, [System.Windows.Forms.Cursor]::Current.Size)
# Get a screenshot
[System.Windows.Forms.Cursors]::Default.Draw($graphic, $cursorBounds)

$rect = New-Object System.Drawing.Rectangle(0, 0, $screen.Width, $screen.Height)



# Iterate through all bytes in image
$data = $image.LockBits($rect, 1, $image.PixelFormat) 
$bmpWidth = $data.Stride
$bytes = $bmpWidth * $data.Height
$rgb = New-Object Byte[] $bytes
$ptr = $data.Scan0

# echo all bytes
echo $rgb