# pyDoomMap

## Description

This is a utility to view Doom maps. You must provide your own .WAD file.

## Usage

At this time the only functionality is to render maps as jpg images.

`python main.py`

Arguments:

- `--wadfile {filename}`: The wad file to read, defaults to `wad/DOOM1.wad`. Relative file path.
- `--mapname {mapname}`: The map to read from the file, defaults to `E1M1`
- `--export_file {filename}`: The relative file path for the export image, defaults to `export/E1M1.jpg`

