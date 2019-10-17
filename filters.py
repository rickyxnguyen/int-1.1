import matplotlib
import matplotlib.pyplot as plt
from skimage import io, filters
import numpy as np

matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['xtick.labelsize'] = 0
matplotlib.rcParams['ytick.labelsize'] = 0


# def split_image_into_channels(image):
#     """Look at each image separately"""
#     red_channel = image[:, :, 0]
#     green_channel = image[:, :, 1]
#     blue_channel = image[:, :, 2]
#     return red_channel, green_channel, blue_channel


# def merge_channels(red, green, blue):
#     """Merge channels back into an image"""
#     return np.stack([red, green, blue], axis=2)

# r, g, b = split_image_into_channels(original_image)
# im = merge_channels(r, g, b)


# def sharpen(image, a, b):
#     """Sharpening an image: Blur and then subtract from original"""
#     blurred = skimage.filters.gaussian_filter(image, sigma=10, multichannel=True)
#     sharper = np.clip(image * a - blurred * b, 0, 1.0)
#     return sharper


# def channel_adjust(channel, values):
#     # preserve the original size, so we can reconstruct at the end
#     orig_size = channel.shape
#     # flatten the image into a single array
#     flat_channel = channel.flatten()

#     # this magical numpy function takes the values in flat_channel
#     # and maps it from its range in [0, 1] to its new squeezed and
#     # stretched range
#     adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

#     # put back into the original image shape
#     return adjusted.reshape(orig_size)