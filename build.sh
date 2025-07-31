#!/bin/bash

# Install FFmpeg
apt-get update && apt-get install -y ffmpeg

# Continue with app start
pip install -r requirements.txt
