#!/bin/bash

# Resize all banners to 300x150
for file in *.jpg; do
    convert $file -resize 300x150 $file
done