"""Contains ShapesBatch class."""

import numpy as np
from skimage.draw import circle, polygon

from batchflow import ImagesBatch, action, inbatch_parallel, any_action_failed


def sample_image(size, min_r, max_r, circles, squares, pixel_value):
    """Generate image with geometrical shapes (circles and squares).
    """
    img = np.zeros((size, size, 2))
    loc = []
    if pixel_value is None:
        vals = np.random.randint(0, 256, circles + squares)
    else:
        vals = [pixel_value] * (circles + squares)
    for f, v in zip(["c"] * circles + ["s"] * squares, vals):
        r = np.random.randint(min_r, max_r + 1)
        xc, yc = np.random.randint(r, size - r + 1, 2)
        if f == "c":
            mask = circle(xc, yc, r, (size, size))
        if f == "s":
            mask = polygon((xc - r, xc + r, xc + r, xc - r),
                           (yc - r, yc - r, yc + r, yc + r), (size, size))
        img[:, :, ["c", "s"].index(f)][mask] = v
        loc.append([xc, yc, r])
    return img, np.array(loc)


class ShapesBatch(ImagesBatch):
    """Contains images with geometrical shapes and masks.
    """
    def __init__(self, index, preloaded=None, *args, **kwargs):
        super().__init__(index, preloaded)

    @action
    @inbatch_parallel(init="indices", post="_assemble_batch")
    def sample_images(self, i, size, min_r=5, max_r=None, circles=1, squares=1, pixel_value=255):
        """Generate images with geometrical shapes.
        """
        if max_r is None:
            max_r = size // 2
        return sample_image(size, min_r, max_r, circles, squares, pixel_value)

    def _reraise_exceptions(self, results):
        """Reraise all exceptions in the ``results`` list.
        """
        if any_action_failed(results):
            all_errors = self.get_errors(results)
            raise RuntimeError("Cannot assemble the batch", all_errors)

    def _assemble_batch(self, results, *args, **kwargs):
        """Concatenate results of different workers.
        """
        _ = args, kwargs
        self._reraise_exceptions(results)
        img, loc = list(zip(*results))
        img = np.stack(img)
        loc = np.stack(loc)
        self.images = np.clip(img.sum(axis=-1, keepdims=True), 0, 255)
        self.labels = loc[:, 0, :2]
        self.masks = np.clip(img[:, :, :, :1], 0, 1).astype(int)
        return self
