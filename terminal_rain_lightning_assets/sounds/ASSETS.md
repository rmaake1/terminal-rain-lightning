# Sound Assets

`rain.mp3` and the thunder MP3 files are based on the sound files contributed
in GitHub PR #1, described there as Pixabay sound effects.

`rain.mp3` was trimmed and re-encoded from the original longer rain file into a
short stereo loop for package size. The loop includes an end-to-start crossfade
so it can repeat under `ffplay -loop 0` without a hard cut.

`thunder.mp3` is the original contributed thunder file from PR #1.
The other `thunder-*.mp3` files are generated variants of that same source,
using pitch, filtering, echo, trimming, and volume adjustments so repeated
lightning strikes do not always trigger the exact same thunder sample.
