#!/bin/bash

# execute docker container with --privileged flag
# invoke this script to get core files in pwntools

echo "core.%e.%p" > /proc/sys/kernel/core_pattern
ulimit -c unlimited
