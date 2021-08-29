
$python   = "py" 
$option   = "run"
$filename = $args[0]

# if( $args[0] -eq $null ) {
#     Write-Host "usage: build.ps1 <script>"
#     exit
# }

$filename = "test.asm"

$output = (Get-Item $filename).Basename + ".o"

$assembler = @("./asm/asm.py", "$filename")
$emulator  = @("./emulator/chip8.py", $output)
$disasm    = @("./disasm/disasm.py", $output)

$all = @($assembler, $emulator)

foreach ($build in $all) {
    Write-Host $build
    & 'py' $build
}
exit