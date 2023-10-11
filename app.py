import pygame
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import random

class Line(object):
    def __init__(self):
        self.WINDOW_WIDTH = 1080
        self.WINDOW_HEIGHT = 720
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.FPS = 60

    def random_rgb_color(_):
        r = random.random()
        g = random.random()
        b = random.random()
       
        return (r, g, b)
    

    def go(self):
        pygame.init()
        screen_width, screen_height = 1600, 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Real-time Audio Visualizer")

        # Create a clock object to control frame rate
        clock = pygame.time.Clock()

        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)

        # Main visualization loop
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read audio data from the microphone
            audio_data = stream.read(self.CHUNK_SIZE)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Clear the screen
            screen.fill((0, 0, 0))

            # Plot the waveform of the microphone input
            c = self.random_rgb_color()

            plt.figure(figsize=(self.WINDOW_WIDTH / 60, self.WINDOW_HEIGHT / 60), facecolor='black')

            plt.plot(audio_array, color=c)
            plt.xlim(0, len(audio_array))
            plt.ylim(-32768, 32768)  # Adjust the y-axis range as needed
            plt.axis('off')

            # Save the plot to a temporary image file
            plt.savefig("temp_plot.png", bbox_inches='tight', pad_inches=0, dpi=100, transparent=True)

            # Load and display the temporary image on the Pygame screen
            plot_img = pygame.image.load("temp_plot.png")
            screen.blit(plot_img, (0, 0))

            # Update the display
            pygame.display.flip()

            # Control frame rate
            clock.tick(self.FPS)

            plt.close()

        # Clean up
        stream.stop_stream()
        stream.close()
        audio.terminate()
        pygame.quit()


if __name__ == "__main__":
    anim = Line()
    anim.go()