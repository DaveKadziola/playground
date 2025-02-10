# Useful commands
___
#### Looking for texts/phrases between ## and ##
- Power Shell
    Get-ChildItem -Path "E:\emptycheck" -Include *.xml, *.config, *.json, *.bat -Recurse | Select-String -Pattern '(?s)(?<=##)[A-Za-z0-9_-]+(?=##)' -AllMatches | Select-Object Filename, LineNumber, @{Name="Match"; Expression={$_.Matches.Value}}
- Bash
    grep -r -P --include='*.xml' --include='*.config' --include='*.json' --include='*.bat' '(?<=##)[A-Za-z0-9_-]+(?=##)' "E:/emptycheck" | awk -F: '{print "Filename: " $1, "LineNumber: " $2, "Match: " $3}'
