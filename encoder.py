#!/usr/bin/env python3

from PIL import Image
import numpy as np
import random
import os
import time
import math

images_folder = "Images" # Images folder needs to be in the same folder as the encoder

def get_rgb(pixel):
    """Safely extract R,G,B even from RGBA."""
    return tuple(map(int, pixel[:3]))

def set_rgb(array, i, j, r, g, b):
    """Write RGB values while preserving alpha if present."""
    pixel = array[i, j]
    if pixel.shape[0] == 3:
        array[i, j] = [r, g, b]
    else:
        array[i, j] = [r, g, b, pixel[3]]

while True: 
    print("\n====== Image Steganography Encoder ======")
    time.sleep(.25)

    # List images from Images folder
    print("\nAvailable images in Images folder: ")
    for f in os.listdir(images_folder):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            print(" -", f)
    time.sleep(.25)

    # Prompt for image name
    filename = input("\nEnter the image filename to encode (or 'exit' to quit): ").strip()
    if filename.lower() == "exit":
        time.sleep(.25)
        print("\nThank you for using our encoder!")
        break

    # Check if file exists
    image_path = os.path.join(images_folder, filename)
    if not os.path.exists(image_path):
        time.sleep(.25)
        print(f"\nFile not found: {image_path}")
        time.sleep(.25)
        continue

    # Load Input Image
    img = Image.open(image_path)
    img_array = np.array(img)
    height, width, _ = img_array.shape

    time.sleep(.25)
    print(f"\nLoaded image shape: {img_array.shape}")

    # Define seed
    seed_bits = "".join(str(random.randint(0, 1)) for _ in range(width))
    random.seed(seed_bits) 

    time.sleep(.25)
    seed_number = int(seed_bits, 2)
    print(f"Seed: {seed_number}")

    # Encode seed in first row
    bit_index = 0

    for x in range(width):
        if bit_index >= len(seed_bits):
            break

        r, g, b = get_rgb(img_array[0, x])
        r = (r & ~1) | int(seed_bits[bit_index])  # modify red channel LSB
        set_rgb(img_array, 0, x, r, g, b)

        bit_index += 1

    time.sleep(.25)
    print("\nSeed successfully encoded in first row")

    # Generate PRNG pattern
    num_pixels = height * width - width
    prng_pattern = [random.randint(1, 3) for _ in range(num_pixels)]

    time.sleep(.25)
    print("Generated pseudorandom pattern for RGB encoding")

    # Get message
    print(f"Max number of characters for the hidden message: {math.floor(num_pixels/8)}")
    time.sleep(.25)
    message = input("\nPlease input your message here: ")

    # Encode message
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    binary_message += "101010101010101010101010"  # exit code
    msg_index = 0

    # Loop through pixels starting at row 1
    for i in range(1, height):
        for j in range(width):
            if msg_index >= len(binary_message):
                break

            bit = int(binary_message[msg_index])
            r, g, b = get_rgb(img_array[i, j])
            channel = prng_pattern[msg_index]

            # Modify correct channel
            if channel == 1:
                r = (r & 254) | bit
            elif channel == 2:
                g = (g & 254) | bit
            else:
                b = (b & 254) | bit

            set_rgb(img_array, i, j, r, g, b)
            msg_index += 1

        if msg_index >= len(binary_message):
            break

    time.sleep(.25)
    print(f"\nMessage of {len(message)} characters encoded successfully!")

    # Save encoded image
    encoded_image = Image.fromarray(img_array)
    output_path = "/".join(image_path.split('/')[:-1]) + "/encoded_" + image_path.split('/')[-1]
    encoded_image.save(output_path)

    time.sleep(.25)
    print(f"Encoded image saved at: {output_path}")
    time.sleep(.25)
