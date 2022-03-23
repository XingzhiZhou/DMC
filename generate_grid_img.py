# coding: utf-8

import sys
import os
import time
import argparse

import numpy as np
import random

from PIL import Image

import json
import util

def pil_grid(imgs, max_horiz=np.iinfo(int).max):
    num_imgs = len(imgs)
    n_horiz = min(num_imgs, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * (num_imgs // n_horiz)
    for i, im in enumerate(imgs):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('RGB', (h_sizes[-1], v_sizes[-1]), color='white')
    for i, im in enumerate(imgs):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid

# Generate 2x2 grid images and a .json file recording the labels
def main():
    
    # Cifar100 paths
    cifar_dir = "./data/cifar100/"
    cifar_image_dir = "./data/cifar100-image/"

    # Load cifar100, get train labels
    _, train_labels = util.load_CIFAR100_train(cifar_dir)
    num_img = train_labels.shape[0]
    num_label = max(train_labels) + 1

    print("Cifar100 (%s) loaded (#image: %d, #label: %d)." % (cifar_dir, num_img, num_label))

    # Input
    # cap_label: The number of labels used to generate grid images
    # gen_coeff: The number of grid images each core image generates

    # Argument parser
    p = argparse.ArgumentParser()
    p.add_argument(
        '-cap_label',  type=int, choices=range(2, num_label), default=8,
        help='The number of labels used to generate grid images (2~%d)' % (num_label))
    p.add_argument(
        '-gen_coeff', type=int, choices=range(1, 101), default=1,
        help='The number of grid images each core image generates (1~100)')
    args = p.parse_args()

    cap_label = args.cap_label
    gen_coeff = args.gen_coeff
    print("cap label: %d, generation coefficient: %d" % (cap_label, gen_coeff))

    # Output paths
    grid_img_dir = "./data/cifar100-grid-image-%d-%d/" % (cap_label, gen_coeff)
    if not os.path.exists(grid_img_dir):
        os.makedirs(grid_img_dir)

    # Grid image generation

    available_labels = list(range(cap_label))

    arr_label_to_imgs = [[] for label in range(num_label)]
    for img, label in enumerate(train_labels):
        arr_label_to_imgs[label].append(img)

    grid_img = -1 # Used as a counter

    arr_grid_img_to_labels = [] # The label of a grid image is an array of labels

    print("Generating grid images...")

    start = time.time()

    for core_img, core_label in enumerate(train_labels):

        util.progress_display(core_img, num_img)

        if(core_label >= cap_label):
            continue

        # For each core image, find 3 other images with different labels (called mate images)
        # Generate a grid image using these 4 images (called member images)       
        for _ in range(gen_coeff):

            grid_img += 1

            core_label = int(core_label) # Convert int32 to int

            candidate_labels = available_labels.copy()
            candidate_labels.remove(core_label)

            mate_labels = random.choices(candidate_labels, k=3)
            mate_imgs = [random.choice(arr_label_to_imgs[mate_label]) for mate_label in mate_labels]

            member_labels = [core_label] + mate_labels
            member_imgs = [core_img] + mate_imgs

            member_img_paths = [(cifar_image_dir + "%d.jpg" % img) for img in (member_imgs)]
            member_img_files = [Image.open(img_path) for img_path in member_img_paths]

            grid_img_file = pil_grid(member_img_files, 2)
            grid_img_file.save(grid_img_dir + 'grid%d.jpg' % grid_img)
            arr_grid_img_to_labels.append(member_labels)

    # Generate a .json file recording labels of grid images
    json_path = grid_img_dir + "labels.json"
    with open(json_path, 'w') as output_json:
        json.dump(arr_grid_img_to_labels, output_json)
    
    end = time.time()
    
    print("\nDone!")
    print("%d grid images generated at %s" % ((grid_img + 1), grid_img_dir))
    print("Time elapse: %.2f sec" % (end - start))

if __name__ == '__main__':
    main()