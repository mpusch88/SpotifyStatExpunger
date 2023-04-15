# Spotify Stat Expunger (endsong History Remover)

## Description

This program is designed to clean up `endsong_*.json` files provided by Spotify to remove unwanted listening history for use in applications such as <h6>stats.fm<h6>. It can be used to remove all songs by a particular artist, or all songs from a particular album, or all songs with a particular title, etc. The only requirement is that the name of the artist, album, or song is unique enough to be not be found in any other song.

## Requirements

- Python 3.x
- Endsong JSON files from Spotify

## Usage

1. Run the program: `python SpotifyStatExpunger.py`
2. Enter the directory path containing the `endsong_*.json` files when prompted.
3. Enter the string to search for within the JSON objects (e.g., artist name, song title, or album title).

The program will then search for matching JSON objects across all the `endsong_*.json` files in the specified directory. It will display the number of matching objects found in each file.

If matching objects are found, you'll be asked whether you want to force all updates (i.e., delete all matching objects without confirmation) or confirm each update individually. To proceed, enter 'y' (yes) or 'n' (no) as appropriate.

The program will then update the `endsong_*.json` files by removing the specified matching objects.

## Notes

- This program uses regular expressions to search for the user-provided string, so it's case-insensitive and can handle variations in spacing.
- Be cautious when using the "force all updates" option, as there is no undo feature once the JSON files have been modified. Creating a backup of the `endsong_*.json` files before running the program is recommended.
