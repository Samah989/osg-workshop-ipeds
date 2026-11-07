#!/bin/bash
echo "Host:        $(hostname)"
echo "Date:        $(date)"
echo "User:        $(whoami)"
echo "Directory:   $(pwd)"
echo "CPUs:        $(nproc)"
echo "Memory (MB): $(free -m | awk '/Mem:/ {print $2}')"
echo "Files here:"
ls -la
