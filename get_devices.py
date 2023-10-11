import sounddevice as sd

print("Available input devices:")
for i, device in enumerate(sd.query_devices()):
    print(i, device['name'])