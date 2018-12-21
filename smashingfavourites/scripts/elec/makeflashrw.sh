#!/bin/sh
case "$1" in
pre)
;;
post)
mount -o remount,rw /flash
;;
esac