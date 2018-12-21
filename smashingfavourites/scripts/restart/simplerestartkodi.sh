#!/bin/sh
case "$1" in
pre)
;;
post)
systemctl restart kodi
;;
esac