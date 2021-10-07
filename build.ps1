function Usage {
    $SCRIPT_NAME = $MyInvocation.MyCommand.Name
    Write-Host "Usage: $($SCRIPT_NAME) [COMMAND] [ARGS]"
    Write-Host "       comp [filename] the path of file"
    Write-Host "            [output]   output file, default is 'a.o'"
    Write-Host "       run             same with compile but it also runs it in the emulator to"
    Write-Host "       test [record]   create binaries from .asm files from the testcases folder"
    Write-Host "            [run]      recompile and compares the new binaries with the testcase binaries"
    exit
}

if($args[0] -eq 'testcases') {
    if($args[1] -eq 'run') {
        $files = Get-ChildItem ".\tests\"
        foreach ($file in $files){
            # $file | Select-Object -Property *
            if($file.Extension -eq '.asm') {
                $output = "$($file.Directory)\$($file.BaseName).out"
                $actual = "$($file.Directory)\$($file.BaseName).test.out"
                
                powershell -command "& py asm.py $($file.FullName) $output"
                
                $testcase = Get-Content $output -Encoding Byte
                $actual   = Get-Content $actual -Encoding Byte

                if(-not (compare $testcase $actual)) {
                    Write-Host "[OK] $($file.Name) passed " -ForegroundColor Green
                } else {
                    Write-Host "[ERROR] testcase $($file.Name) has changed" -ForegroundColor Red
                }
            }
        }

    }

    if($args[1] -eq 'record') {
        $files = Get-ChildItem ".\tests\"
        foreach ($file in $files){
            # $file | Select-Object -Property *
            if($file.Extension -eq '.asm') {
                $testcase = "$($file.Directory)\$($file.BaseName).test.out"
                powershell -command "& py asm.py $($file.FullName) $testcase"
                Write-Host "[OK] Create testcase: $testcase" -ForegroundColor green
            }
        }
    }
}
elseif($args[0] -eq 'run') {
    $filename = $args[1]
    $output    = "a.out"
    $assembler = @("./asm.py",    $filename, $output)
    $emulator  = @("./chip8.py",  $output)

    del $output | Out-Null
    $all = @($assembler, $emulator)

    foreach ($build in $all) {
        Write-Host '[RUN] py' $build -ForegroundColor Green
        & 'py' $build
    }
}
else { Usage }

# Some other useful commands
# py .\disasm.py .\output.ch8  | Out-File -FilePath .\test1.asm -Encoding ASCII
