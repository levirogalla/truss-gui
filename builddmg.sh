#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Truss Maker.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Truss Maker.dmg" && rm "dist/Truss Maker.dmg"
create-dmg \
  --volname "Truss Maker" \
  --volicon "./misc/appicon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Truss Maker.app" 175 120 \
  --hide-extension "Truss Maker.app" \
  --app-drop-link 425 120 \
  "dist/Truss Maker.dmg" \
  "dist/dmg/"