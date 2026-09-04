# Cinematic Image Reveal Effect

A Python script using OpenCV and NumPy that generates a stunning, 20-second cinematic reveal animation from a single image. Designed perfectly for capturing high-retention content for Instagram Reels, YouTube Shorts, or TikTok.

The script traces the glowing golden outlines of the subject before smoothly crossfading into the full-color image, all while a continuous shower of golden sparkles falls over a dynamic, blurred background.

## Features

* **Golden Skeleton Tracing:** Intelligently detects the most prominent contours of the subject and draws them sequentially over time to build a glowing outline.
* **Dynamic Blurred Background:** Automatically generates a widescreen 16:10 background using a heavily blurred, darkened version of the source image to eliminate harsh black borders.
* **Falling Sparkle Particle System:** Features an optimized background particle system generating glowing, falling golden dust that resets seamlessly.
* **Smooth Crossfade:** 4-second luxurious crossfade transition from the neon skeleton sketch to the final high-resolution image.
* **Mac-Optimized Fullscreen:** Uses a 1920x1200 resolution with specific OpenCV flags to achieve true borderless fullscreen on 16:10 Mac displays without menu bar clipping.

## Requirements

You need Python 3 installed along with the following libraries:

```bash
pip install opencv-python numpy

```

*Note: It is recommended to run this within a virtual environment (e.g., `venv311`).*

## Usage

1. Clone or download this repository.
2. Ensure your target image is in the same directory as the script and named `balaji.png` (or update the `INPUT_IMAGE` variable in the script to match your file name).
3. Run the script:

```bash
python balaji.py

```

*Note: The script will open a fullscreen window immediately. Press `q` or `ESC` at any time to exit the animation early.*

## Configuration

You can easily tweak the look and feel of the animation by modifying the variables at the top of the script:

* **Timings:** Adjust `REVEAL_SECONDS`, `CROSSFADE_SECONDS`, and `HOLD_SECONDS` to change the pacing of the video.
* **Resolution:** Modify `CANVAS_W` and `CANVAS_H` if you are using a standard 16:9 monitor (e.g., `1920x1080`) instead of a Mac screen.
* **Particles:** Change `SPARKLE_COUNT` to increase or decrease the density of the falling golden dust.
