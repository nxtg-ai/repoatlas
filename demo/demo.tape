# VHS tape for Atlas terminal demo
# Install VHS: https://github.com/charmbracelet/vhs
# Usage: vhs demo/demo.tape

Output demo/demo.gif
Output demo/demo.webm

Set Shell "bash"
Set FontSize 14
Set Width 1200
Set Height 800
Set Theme "Catppuccin Mocha"
Set Padding 20
Set TypingSpeed 40ms
Set PlaybackSpeed 1.5

Sleep 500ms

Type "atlas status"
Enter
Sleep 5s

Type "atlas connections"
Enter
Sleep 4s

Type "atlas inspect atlas"
Enter
Sleep 4s
