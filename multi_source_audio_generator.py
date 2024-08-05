import pyroomacoustics as pra
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from scipy.io import wavfile
import soundfile as sf

# Read the input audio file
fs, audio = wavfile.read("input.wav")

# Convert to mono if the audio is stereo
if audio.ndim > 1:
    audio = np.mean(audio, axis=1)

# Define room dimensions and create a room
room_dim = np.array([1000, 1000, 1000])  # Large room dimensions
room = pra.ShoeBox(room_dim, fs=fs, max_order=0)  # Simulate infinite room

# Generate random positions for the source and microphone
source_position = room_dim * 0.75
mic_position = room_dim * 0.25

# Add the source with a signal and delay
room.add_source(source_position, signal=audio)

# Add the microphone array
mic_array_positions = np.array(
    [
        [mic_position[0], mic_position[1], mic_position[2] + 0.03],
        [mic_position[0] + 0.03, mic_position[1], mic_position[2]],
        [mic_position[0], mic_position[1] + 0.03, mic_position[2]],
    ]
)

room.add_microphone_array(mic_array_positions.T)

print(f"Source position: {source_position}")
print(f"Microphone positions: {mic_array_positions}")

room.simulate()

recorded_signals = room.mic_array.signals


# Save the recorded signals
output_path = "recorded_sound"
os.makedirs(output_path, exist_ok=True)

# Plot the recorded signals
plt.figure(figsize=(10, 6))
for i, signal in enumerate(recorded_signals):
    plt.subplot(len(recorded_signals), 1, i + 1)
    plt.plot(signal)
    plt.title(f"Recorded Signal at Microphone {i + 1}")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
plt.tight_layout()
plt.savefig(f"{output_path}/signal_graph.png")


for i, signal in enumerate(recorded_signals):
    sf.write(f"{output_path}/recorded_signal_mic_{i + 1}.wav", signal, room.fs)

# Plot the room layout
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

# Plot room dimensions
room_corners = np.array(
    [
        [0, 0, 0],
        [room_dim[0], 0, 0],
        [room_dim[0], room_dim[1], 0],
        [0, room_dim[1], 0],
        [0, 0, room_dim[2]],
        [room_dim[0], 0, room_dim[2]],
        [room_dim[0], room_dim[1], room_dim[2]],
        [0, room_dim[1], room_dim[2]],
    ]
)
for i in range(4):
    ax.plot(
        [room_corners[i][0], room_corners[(i + 1) % 4][0]],
        [room_corners[i][1], room_corners[(i + 1) % 4][1]],
        [room_corners[i][2], room_corners[(i + 1) % 4][2]],
        "k--",
    )

for i in range(4, 8):
    ax.plot(
        [room_corners[i][0], room_corners[i - 4][0]],
        [room_corners[i][1], room_corners[i - 4][1]],
        [room_corners[i][2], room_corners[i - 4][2]],
        "k--",
    )

# Plot source
ax.scatter(*source_position, color="r", s=100, label="Source")

# Plot microphones
for i, mic in enumerate(mic_array_positions):
    ax.scatter(*mic, s=100, label=f"Microphone {i + 1}")

# Draw lines connecting microphones
num_mics = len(mic_array_positions)
for i in range(num_mics):
    for j in range(i + 1, num_mics):
        ax.plot(
            [mic_array_positions[i, 0], mic_array_positions[j, 0]],
            [mic_array_positions[i, 1], mic_array_positions[j, 1]],
            [mic_array_positions[i, 2], mic_array_positions[j, 2]],
            "b-",
        )

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Room Layout with Source and Microphones")
ax.legend()
plt.savefig(f"{output_path}/room_layout.png")
