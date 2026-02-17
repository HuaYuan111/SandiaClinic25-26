#!/usr/bin/env python3
"""
IDPP Interpolation Script using ASE
Generates intermediate images between two structures using
Image Dependent Pair Potential (IDPP) for NEB calculations.
"""

from ase.io import read, write
from ase.neb import NEB
from ase.optimize import BFGS
from ase.neb.idpp import interpolate

import sys
import os

def main():
    if len(sys.argv) != 5:
        print("Usage: python idpp_interpolation.py initial.xyz final.xyz n_images output_dir")
        sys.exit(1)

    initial_file = sys.argv[1]
    final_file = sys.argv[2]
    try:
        n_images = int(sys.argv[3])
        if n_images < 2:
            raise ValueError
    except ValueError:
        print("Error: n_images must be an integer >= 2")
        sys.exit(1)

    output_dir = sys.argv[4]
    os.makedirs(output_dir, exist_ok=True)

    # Read initial and final structures
    try:
        initial = read(initial_file)
        final = read(final_file)
    except Exception as e:
        print(f"Error reading input files: {e}")
        sys.exit(1)

    # Create images list for NEB
    images = [initial]
    for _ in range(n_images - 2):
        images.append(initial.copy())
    images.append(final)

    # Linear interpolation first
    neb = NEB(images)
    neb.interpolate()

    # Apply IDPP interpolation to improve path
    interpolate(images)

    # Save interpolated images
    for i, img in enumerate(images):
        out_path = os.path.join(output_dir, f"image_{i:02d}.xyz")
        write(out_path, img)
        print(f"Saved: {out_path}")

    print("IDPP interpolation completed successfully.")

if __name__ == "__main__":
    main()
