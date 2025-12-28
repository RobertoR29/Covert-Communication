#!/usr/bin/env/ python3

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.io import imread
import sys

def metrics(path1, path2):
    #Load both images
    try: 
        img1 = imread(path1)
        img2 = imread(path2)
    except FileNotFoundError as e:
        print(f"\nError! {e}\n")
        return

    #Ensure they have the same shape
    if img1.shape != img2.shape:
        print(f"\nImages must have the same dimensions for comparison.\n{path1} shape: {img1.shape}, {path2} shape: {img2.shape}\n")
        return

    #Compute PSNR
    psnr_result = psnr(img1, img2, data_range=img1.max() - img1.min())

    #Compute SSIM
    ssim_result = ssim(img1, img2, channel_axis=-1)

    print(f"\nPSNR: {psnr_result:.2f} dB")
    print(f"SSIM: {ssim_result:.4f}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python metrics.py <image1> <image2>")
        sys.exit(1)

    metrics(sys.argv[1], sys.argv[2])
