Python script to convert playlists from older PlyCast versions (1.0.4.3) into the new format (Version 1.0.27.x) 

**Usage:

*Convert one playlist
python convert_plycast.py playlist.plyt

Output: playlist_new.plyt

**Convert whole folder
python convert_plycast.py C:\Playlists

**Output: C:\Playlists_new\

**Keep old IDs instead of random GUIDs
python convert_plycast.py playlist.plyt --guid keep
