#!/bin/bash
filename=day_$(date +%d).py
cp --update=none template.py $filename
chmod +x $filename
pdm run nvim $filename
