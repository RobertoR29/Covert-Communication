#!/usr/bin/env python3

from PIL import Image
import numpy as np
import random
import os
import time

images_folder = "Images"  # Images folder needs to be in the same folder as the encoder.

def get_rgb(pixel):
    """Safely extract R,G,B even from an RGBA pixel."""
    return tuple(map(int, pixel[:3]))

while True: 
    print("\n====== Image Steganography Decoder ======")
    time.sleep(.25)

    # List images from Images folder
    print("\nAvailable images in Images folder: ")
    for f in os.listdir(images_folder):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            print(" -", f)
    time.sleep(.25)

    # Prompt user for image filename
    filename = input("\nEnter the image filename to decode (or 'exit' to quit): ").strip()
    if filename.lower() == "exit":
        time.sleep(.25)
        print("\nThank you for using our decoder!")
        break

    # Check if file exists
    image_path = os.path.join(images_folder, filename)
    if not os.path.exists(image_path):
        time.sleep(.25)
        print(f"\nFile not found: {image_path}")
        time.sleep(.25)
        continue

    # Load encoded image
    img = Image.open(image_path)
    img_array = np.array(img)
    height, width, channels = img_array.shape

    time.sleep(.25)
    print(f"\nLoaded image shape: {img_array.shape}")

    # Step 1 — Extract seed bits from the first row (RED channel LSB)
    seed_bits = ''.join(str(int(img_array[0, x][0]) & 1) for x in range(width))

    time.sleep(.25)
    seed_number = int(seed_bits, 2)
    print(f"Extracted Seed: {seed_number}")

    # Step 2 — Re-seed PRNG
    random.seed(seed_bits)

    # Step 3 — Reconstruct PRNG pattern
    num_pixels = height * width - width
    prng_pattern = [random.randint(1, 3) for _ in range(num_pixels)]

    # Step 4 — Extract message bits
    binary_message = ""
    msg_index = 0

    for i in range(1, height):
        for j in range(width):
            if msg_index >= len(prng_pattern):
                break

            # Stop if exit code is detected
            if binary_message.endswith("101010101010101010101010"):
                break

            r, g, b = get_rgb(img_array[i, j])
            channel = prng_pattern[msg_index]

            if channel == 1:
                bit = r & 1
            elif channel == 2:
                bit = g & 1
            else:
                bit = b & 1

            binary_message += str(bit)
            msg_index += 1

        if msg_index >= len(prng_pattern):
            break

    # Step 5 — Convert binary to ASCII
    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) < 8:
            break

        char = chr(int(byte, 2))

        # Stop at invalid ASCII
        if char not in ''.join(map(chr, range(32, 127))):
            break

        decoded_message += char

    time.sleep(.25)
    print(f"\nDecoded message: {decoded_message}")
    print(f"\nLength of message: {len(decoded_message)}")
