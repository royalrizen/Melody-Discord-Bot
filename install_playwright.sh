#!/usr/bin/env bash
set -e

# Set PLAYWRIGHT_BROWSERS_PATH
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/playwright

# Install Playwright with Chromium
pip install playwright
playwright install chromium

# Manage Playwright cache
if [ ! -d "$PLAYWRIGHT_BROWSERS_PATH" ]; then
  echo "...Storing Playwright Cache in Build Cache"
  cp -R $XDG_CACHE_HOME/playwright/ $PLAYWRIGHT_BROWSERS_PATH
else
  echo "...Copying Playwright Cache from Build Cache"
  cp -R $PLAYWRIGHT_BROWSERS_PATH $XDG_CACHE_HOME
fi
