#!/bin/bash

# Script to rewrite git history commit messages to follow conventional commit standards
# Lowercases the first line and truncates to 60 characters

git filter-branch --msg-filter '
    read msg
    first_line=$(echo "$msg" | head -n1 | tr "[:upper:]" "[:lower:]" | cut -c1-60)
    rest=$(echo "$msg" | tail -n +2)
    echo "$first_line
$rest"
' -- --all