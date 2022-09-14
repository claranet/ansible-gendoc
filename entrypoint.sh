#!/bin/sh
# Read in the file of environment settings
. /etc/profile
# Then run the CMD
exec ansible-gendoc "$@"
