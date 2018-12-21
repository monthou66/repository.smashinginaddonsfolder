#!/bin/sh
case "$1" in
pre)
;;
post)
mount -o remount,rw /flash
rm /flash/menu.lst
rm /flash/libreelec.txt
cp /flash/stuff/menus/windows/menu.lst /flash/menu.lst
cp /flash/stuff/menus/windows/libreelec.txt /flash/libreelec.txt
mount -o remount,ro /flash
reboot
;;
esac