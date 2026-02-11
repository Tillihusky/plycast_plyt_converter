# Python script to convert playlists from older PlyCast versions (1.0.4.3) into the new format (Version 1.0.27.x) 

## Usage:

**Single file (new random GUIDs like PlyCast 1.0.27.3-rc exports):**
`python convert_plycast.py old.xml` 


**Keep old IDs (convert to dashed format instead of new random UUIDs):**
`python convert_plycast.py old.xml --guid keep` 


**Convert a whole folder:**
`python convert_plycast.py "C:\playlists\old"  "C:\playlists\new"`
