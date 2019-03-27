"""Contains a batch class to segmentation task."""
import numpy as np
from PIL import Image

from batchflow import ImagesBatch, action, inbatch_parallel


class MnistBatch(ImagesBatch):
    """
    Batch can create images with specified size and noisy with parts of other digits.
    """
    components = 'images', 'labels', 'masks', 'big_img'

    @inbatch_parallel(init='indices')
    def _paste_img(self, ix, coord, size, src, dst):
        img = self.get(ix, src) if src != 'labels' else Image.new('L', (28, 28), color=1)
        img.thumbnail(size, Image.ANTIALIAS)
        new_img = Image.new("L", size, "black")
        i = self.get_pos(None, src, ix)
        new_img.paste(img, [*coord[i]])
        getattr(self, dst)[i] = new_img

    @action
    def create_big_img(self, coord, shape, src='images', dst='big_img'):
        """Creation image with specified size and put the image from batch to a random place.
        Parameters
        ----------
        coord : list with size 2
            x and y cooridates of image position
        shape : int or list
            crated image's shape
        src : str
            component's name from which the data will be obtained
        dst : str
            component's name into which the data will be stored

        Returns
        -------
            self
        """
        shape = [shape]*2 if isinstance(shape, int) else shape
        for sour, dest in zip(src, dst):
            if getattr(self, dest) is None:
                setattr(self, dest, np.array([None] * len(self.index)))
            self._paste_img(coord, shape, sour, dest)
        return self

    @action
    @inbatch_parallel(init='indices')
    def add_noize(self, ix, num_parts=80, src='big_img', dst='big_img'):
        """Adding the parts of numbers to the image.
        Parameters
        ----------
        num_parts : int
            The number of the image's parts
        src : str
            component's name from which the data will be obtained
        dst : str
            component's name into which the data will be stored
        """
        img = self.get(ix, src)
        ind = np.random.choice(self.indices, num_parts)
        hight, width = np.random.randint(1, 5, 2)
        coord_f = np.array([np.random.randint(10, 28-hight, len(ind)), \
                            np.random.randint(10, 28-width, len(ind))])

        coord_t = np.array([np.random.randint(0, img.size[0]-hight, len(ind)), \
                            np.random.randint(0, img.size[1]-width, len(ind))])

        for i, num_img in enumerate(np.array(ind)):
            crop_img = self.get(num_img, 'images')
            crop_img = crop_img.crop([coord_f[0][i], coord_f[1][i], \
                                      coord_f[0][i]+hight, coord_f[1][i]+width])
            img.paste(crop_img, list(coord_t[:, i]))
            local_ix = self.get_pos(None, dst, ix)
            getattr(self, dst)[local_ix] = img
