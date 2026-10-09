import os
import numpy as np
from PIL import Image, ImageDraw

def generate_noisy_satellite_dataset(folder_name="noisy_data", num_images=10):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    width, height = 400, 400

    # 1. Create the base "Clean" Image (a simple planet/moon over a dark background)
    base_img = Image.new('RGB', (width, height), color=(10, 10, 30))
    draw = ImageDraw.Draw(base_img)
    # Draw a "planet"
    draw.ellipse([100, 100, 300, 300], fill=(80, 150, 200))
    # Draw some "stars"
    for _ in range(50):
        sx, sy = np.random.randint(0, width), np.random.randint(0, height)
        draw.point((sx, sy), fill=(255, 255, 255))

    base_array = np.array(base_img, dtype=np.float32)

    # 2. Generate noisy variations
    for i in range(num_images):
        # Copy the base image
        img_variation = base_array.copy()

        # Add random Gaussian noise (Sensor Noise)
        noise = np.random.normal(loc=0, scale=40, size=img_variation.shape)
        img_variation = img_variation + noise

        # Clip values to valid RGB range [0, 255]
        img_variation = np.clip(img_variation, 0, 255).astype(np.uint8)

        # Convert back to Pillow image to draw transient streaks
        noisy_pil = Image.fromarray(img_variation)
        draw_noisy = ImageDraw.Draw(noisy_pil)

        # Add a random "Satellite Streak" (Transient Artifact)
        start_x = np.random.randint(0, width)
        start_y = np.random.randint(0, height)
        end_x = start_x + np.random.randint(-200, 200)
        end_y = start_y + np.random.randint(-200, 200)

        draw_noisy.line([(start_x, start_y), (end_x, end_y)], fill=(255, 255, 255), width=3)

        # Save to folder
        file_path = os.path.join(folder_name, f"noisy_frame_{i+1:03d}.png")
        noisy_pil.save(file_path)
        print(f"Generated: {file_path}")

# Run the generator
generate_noisy_satellite_dataset(num_images=10)
