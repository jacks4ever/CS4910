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
1. **Initial State**: Audio shows "⏸️ Click to Enable" (yellow)
2. **User Interaction**: Click anywhere, press a key, or touch the screen
3. **Audio Enabled**: Status changes to "🔊 Ready" (green)
4. **Sound Effects**: Glass break and overheat sounds will now play during attacks

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
1. Load the dashboard in your browser
2. Click the **"🔊 Test Sound"** button in the status bar
3. Check the browser console (F12) for debug messages
4. You should hear a beep followed by a glass break sound

### Full Attack Simulation:
1. Click **"⚠️ Simulate Attack"** to trigger fake exploit detection
2. This will test the complete audio sequence during actual attacks

### Manual Testing Steps:
1. **Click "🎵 Enable Audio"** in the status bar (or click anywhere/press a key) to satisfy browser policies
2. **Audio status should change** from "⏸️ Click to Enable" to "🔊 Ready"
3. **Use test buttons** to verify audio works
4. **Check browser console** for detailed debug information

### Expected Behavior:
- **First interaction**: Audio context initializes
- **Test Sound button**: Plays beep + glass break
- **Simulate Attack**: Triggers full attack sequence with sounds
- **Real attacks**: Automatic sound effects during live detection