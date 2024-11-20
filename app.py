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
        self.lines = []

        pygame.init()
        pygame.display.set_caption("Real-time Audio Visualizer")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    def random_rgb_color(_):
        r = random.random()
        g = random.random()
        b = random.random()
       
        return (r, g, b)
    
    def draw_lines(self):
        for line in self.lines:
            x1, y1, x2, y2, color = line
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 2)
    
    def update_plot(self, audio_data):
        # Calculate the volume (root mean square)
        volume = np.sqrt(np.mean(audio_data**2))
        
        if volume > 1:
            # Random starting point
            line_x1 = np.random.randint(0, self.WINDOW_WIDTH)
            line_y1 = np.random.randint(0, self.WINDOW_HEIGHT)
            
            # Random color
            color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
            
            # Calculate line length based on volume
            line_length = int(volume * 1.5)  # Adjust the multiplier for line length
            
            # Random line angle
            line_angle = np.random.uniform(0, 2 * np.pi)
            
            line_x2 = line_x1 + line_length * np.cos(line_angle)
            line_y2 = line_y1 + line_length * np.sin(line_angle)
            
            # Add the new line to the list
            self.lines.append((line_x1, line_y1, line_x2, line_y2, color))
            
            if len(self.lines) > 5:
                self.lines.pop(0)
            
            # self.draw_lines()

    def go(self):

        # Create a clock object to control frame rate

        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK_SIZE, input_device_index=2)

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
            self.screen.fill((0, 0, 0))

            # Plot the waveform of the microphone input
            c = self.random_rgb_color()

            plt.figure(figsize=(self.WINDOW_WIDTH / 60, self.WINDOW_HEIGHT / 60), facecolor='black')

            plt.plot(audio_array, color=c)
            plt.xlim(0, len(audio_array))
            plt.ylim(-32768, 32768)  # Adjust the y-axis range as needed
            plt.axis('off')

            # Save the plot to a temporary image file
            plt.savefig("./venv/temp_plot.png", bbox_inches='tight', pad_inches=0, dpi=100, transparent=True)

            # Load and display the temporary image on the Pygame screen
            plot_img = pygame.image.load("./venv/temp_plot.png")
            
            
            self.screen.blit(plot_img, (0, 0))

            self.update_plot(audio_array)

            # Update the display
            pygame.display.flip()
            pygame.display.update()

            # Control frame rate
            self.clock.tick(self.FPS)

            plt.close()

        # Clean up
        stream.stop_stream()
        stream.close()
        audio.terminate()
        pygame.quit()


if __name__ == "__main__":
    anim = Line()
    anim.go()