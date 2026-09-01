#!/usr/bin/env bash
# Lunar Field Cards — local preview server
python3 -m http.server -b localhost 8002
lsof -i :8002
