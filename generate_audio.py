import sys
from pydub import AudioSegment
import moviepy.editor as mp

# Get video filename from command-line argument
if len(sys.argv) < 2:
    print("Usage: python generate_audio.py <video_file>")
    sys.exit(1)

video_file = sys.argv[1]  # Get video filename dynamically

# Load original audio files
left_audio = AudioSegment.from_wav("left_turn.wav")
right_audio = AudioSegment.from_wav("right_turn.wav")

# Get actual video duration
video = mp.VideoFileClip(video_file)
video_duration = video.duration  # Get video duration in seconds

# Initialize an empty audio track (same length as video)
final_audio = AudioSegment.silent(duration=int(video_duration * 1000))

# Load saved audio timestamps from a file
audio_events = []
with open("audio_events.txt", "r") as file:
    for line in file:
        timestamp, direction = line.strip().split(",")
        audio_events.append((float(timestamp), direction))

# Overlay audio clips at correct timestamps
for timestamp, direction in audio_events:
    audio_clip = left_audio if direction == 'L' else right_audio
    start_time_ms = int(timestamp * 1000)  # Convert seconds to milliseconds
    final_audio = final_audio.overlay(audio_clip, position=start_time_ms)

# Save the final combined audio file
final_audio.export("final_audio.wav", format="wav")
print(f"Final audio generated as final_audio.wav (duration: {video_duration:.2f} seconds)")
