import matplotlib.pyplot as plt
import numpy as np
import napari
import dask.array as da


def blended_img(viewer, index=(Ellipsis), use_viewer_clims = True, percentile_clim=False, contrast_limits=(2, 99.5)):
    """insert doc string"""
    blended = np.zeros(viewer.layers[0].data[index].shape + (4,))
    colormapped_list = list()
    for layer in viewer.layers:
        img = layer.data[index]
        if isinstance(img, da.core.Array):
            img = img.compute()

        # normalize data by clims
        if use_viewer_clims is True and percentile_clim is False:
            normalized_data = (img - layer.contrast_limits[0]) / (
            layer.contrast_limits[1] - layer.contrast_limits[0]
        )

        if percentile_clim is True:
            if img.max() == 0:
                normalized_data = img 
            else:
                normalized_data = (img - np.percentile(img.ravel(), contrast_limits[0])) / (
                np.percentile(img.ravel(), contrast_limits[1]) - np.percentile(img.ravel(), contrast_limits[0]
        ))
        colormapped_data = layer.colormap.map(normalized_data.flatten())
        colormapped_data = colormapped_data.reshape(normalized_data.shape + (4,))
        colormapped_list.append(colormapped_data)
        blended = blended + colormapped_data

    blended[..., 3] = 1

    colormapped_list.append(blended)
    return colormapped_list


def create_matplotlib_figure(viewer, title_tup, index, **kwargs):
    title_list = [title + ("composite",) for title in title_tup]
    days_of_stainings = viewer.layers[0].data.shape[0]

    fig, ax = plt.subplots(
        nrows=days_of_stainings, ncols=len(viewer.layers) + 1, figsize=(12, 15)
    )

    for day in range(days_of_stainings):
        img_list = blended_img(viewer, (day,) + index, **kwargs)
        for i, img in enumerate(img_list):
            ax[day, i].imshow(img)
            ax[day, i].axis("off")
            ax[day, i].set_title(title_list[day][i])
