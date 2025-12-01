# Audio Files for Exploit Detection Dashboard

This directory can optionally contain audio files for enhanced sound effects. If audio files are not present, the dashboard will automatically use Web Audio API generated sounds as fallbacks.

## Automatic File Detection

- The frontend now checks for these files at runtime before loading them.
- If the files exist, the HTML5 `<audio>` elements stream them normally.
- If they are missing, no network requests are made (so no 404 spam) and Web Audio fallbacks provide synthesized effects instead.
- You can drop replacement files into this folder at any time and refresh the page; the detection logic will pick them up automatically.

## Optional Audio Files:

### glass_break.mp3 / glass_break.wav
- **Purpose**: Plays when cracks appear on the victim computer screen
- **Timing**: Each time a new crack is added (7 times total)
- **Suggested**: Short glass shattering sound (0.5-1 second)
- **Volume**: Moderate (0.6 volume setting)
- **Fallback**: Web Audio API now renders a stereo, multi-layer glass shatter via `OfflineAudioContext` with noise bursts, shard chirps, and cabinet thud for a more realistic effect

### overheat.mp3 / overheat.wav
- **Purpose**: Plays when victim computer turns red and overheats (7th exploit)
- **Timing**: Starts when computer becomes "destroyed" and overheats
- **Suggested**: Continuous electronic overheating/burning sound with crackling
- **Volume**: Lower background effect (0.4 volume setting)
- **Loop**: Yes (continues during celebration)
- **Fallback**: Web Audio API generates a crackling electronic sound

### Pacman-death-sound.mp3
- **Purpose**: Plays once when the 7th (final) exploit shatters the victim monitor.
- **Timing**: Fires alongside the glass-break effect that completes the destruction sequence.
- **Suggested**: Keep the provided retro "Pac-Man death" sample for instant nostalgia cues.
- **Volume**: Slightly louder foreground sting (0.8 volume setting) layered on top of the glass break.
- **Fallback**: Web Audio API recreates a quick descending chiptune arpeggio if the MP3 is missing.
- **Notes**: Ships as `sounds/Pacman-death-sound.mp3`, auto-detected the same way as the other optional assets.

## Audio File Sources:

You can find free sound effects at:
- [Freesound.org](https://freesound.org)
- [Zapsplat.com](https://www.zapsplat.com)
- [Soundjay.com](https://www.soundjay.com)

Search terms:
- "Glass break" or "glass shatter"
- "Computer overheat" or "electronic burn" or "circuit fry"

## File Format:
- MP3 preferred for smaller file size
- WAV as fallback
- Keep files under 500KB each for web performance

## Browser Audio Requirements:

### Modern Browser Policies:
- **User Interaction Required**: Browsers require user interaction (click, keypress, touch) before playing audio
- **HTTPS Recommended**: Some browsers require HTTPS for Web Audio API
- **Autoplay Blocked**: Automatic audio playback is blocked without user consent

### How It Works:
1. **Page Load**: Audio elements pre-load any optional MP3/WAV files automatically (no toggle needed).
2. **Browser Consent**: Click anywhere, press a key, or touch the screen once after load to satisfy autoplay policies.
3. **Automatic Playback**: After that first interaction, every exploit-driven event (glass break, overheat, Pac-Man sting) plays without further action.

### Troubleshooting:
- If sounds don't play, try clicking anywhere on the page first
- Check browser console for error messages
- Ensure browser allows audio playback for the site
- Try refreshing the page and interacting again

## Browser Compatibility:
- Modern browsers with Web Audio API support will work automatically
- Audio files enhance the experience but are not required
- Sound effects respect browser autoplay policies and user interaction requirements

## Testing Audio

### Quick Audio Test:
1. Load the dashboard in your browser and click anywhere once to unlock audio playback.
2. Open DevTools (F12) and run `playGlassBreakSound();` in the console to trigger the glass shatter cue manually.
3. Optionally run `playPacmanDeathSound();` to preview the final exploit sting.
4. Watch the console for confirmation messages (e.g., "Glass break sound played successfully").

### Full Attack Simulation:
1. Run the backend detector and generate real attack traffic (or replay the sample test traffic) so the server emits `attack_detected` events
2. When a live exploit fires, the dashboard will exercise the complete visual + audio sequence automatically

### Manual Testing Steps:
1. **Interact once** (click/key/touch) immediately after the dashboard loads to unlock audio.
2. **Generate traffic** by running the backend detector plus sample traffic (`test_traffic.py`) so real `attack_detected` events fire.
3. **Observe logs** in the browser console for audio messages if you need to verify playback details.

### Expected Behavior:
\- **First interaction**: Audio context initializes as soon as you interact with the page.
\- **Manual console call (optional)**: Running `playGlassBreakSound()` or `playPacmanDeathSound()` triggers the corresponding cue immediately.
\- **Real attacks**: Automatic sound effects fire during live detection once the browser has been unlocked.

## Bundled Glass Break Sample

- `sounds/glass_break.wav` now ships with the dashboard so you have a natural glass-shatter reference without hunting for assets.
- **Source**: Clip `1-20133-A-39.wav` from the [ESC-50 environmental sound dataset](https://github.com/karoldvl/ESC-50) curated by Karol J. Piczak.
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0). See the [license summary](https://creativecommons.org/licenses/by/4.0/) for details.
- **Required credit** (include somewhere in your report or demo video):
	`Glass breaking sample "1-20133-A-39.wav" © Karol J. Piczak / ESC-50 (CC BY 4.0)`
- The frontend automatically discovers this `.wav` via the existing optional-audio probe logic, so no code changes are necessary—just keep the file in `frontend/sounds/`.

## Bundled Pac-Man Death Sample

- `sounds/Pacman-death-sound.mp3` ships with the dashboard to add the classic arcade "character defeated" sting when the final exploit lands.
- **Source**: [Pacman Death Sound](https://orangefreesounds.com/pacman-death-sound/) by Alexander via Orange Free Sounds.
- **License**: Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). See the [license text](https://creativecommons.org/licenses/by-nc/4.0/) for allowed uses.
- **Required credit** (include alongside your glass-break attribution):
	`"Pacman Death Sound" © Alexander / Orange Free Sounds (CC BY-NC 4.0)`
- Usage is limited to non-commercial course/demo scenarios. For commercial work, obtain a different asset.