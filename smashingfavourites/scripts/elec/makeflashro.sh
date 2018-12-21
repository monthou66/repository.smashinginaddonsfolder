#!/bin/sh
case "$1" in
pre)
;;
post)
mount -o remount,ro /flash
;;
esac