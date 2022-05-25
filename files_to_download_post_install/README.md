# Things to do Post Install

## The situation

I want to dualboot both Arch Linux and Windows, and be able to access both OS's through GRUB. Unfortunately, I installed a BIOS boot partition 
when Windows uses EFI, so I can't do that.

## The Solution

Very Janky, but I am going to reinstall Arch Linux. I will upload the config files I have to Github, so I can copy and paste them into my confg post install. 

Dependencies to add post-install:
```
sudo pacman -S kitty qtile light
```

So yes, that's the plan.

Don't forget to do the following:
```
sudo chmod +x autostart.sh
sudo chmod +s /usr/bin/light
```
