# linuxconfig
Stuff for my workstations

## statusbar.py
Add the following config to your ~/.config/sway/config:  
```py
bar {
    position top
    status_command python3.7 ~/Documents/projects/linuxconfig/statusbar.py
    colors {
        statusline #ffffff
        background #323232
        inactive_workspace #32323200 #32323200 #5c5c5c
    }
}
``` 
