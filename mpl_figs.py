import matplotlib.pyplot as plt
import numpy as np
import napari
import dask.array as da


def blended_img(
    viewer,
    index=(Ellipsis),
    contrast_limits=None,
):
    """Creates blended image

    Args:
        viewer (napari viewer object]): [description]
        index (tuple, optional): [description]. Defaults to (Ellipsis).
        contrast_limits: Defaults to None and uses viewer contrast limits.
        If tuple passed, uses this for percentage contrast limits. If list passed, set contrast limits from list.

    Returns:
        colormapped_list: list of RGB images
        clims_used: list of contrast limits used
    """
    blended = np.zeros(viewer.layers[0].data[index].shape + (4,))
    colormapped_list = list()
    clims_used = list()
    for i, layer in enumerate(viewer.layers):
        img = layer.data[index]
        if isinstance(img, da.core.Array):
            img = img.compute()

        # normalize data by clims
        if contrast_limits is None:
            lower_clim = layer.contrast_limits[0]
            upper_clim = layer.contrast_limits[1]
            normalized_data = (img - lower_clim) / (upper_clim - lower_clim)

        if isinstance(contrast_limits, tuple):
            if img.max() == 0:
                normalized_data = img
            else:
                lower_clim = np.percentile(img.ravel(), contrast_limits[0])
                upper_clim = np.percentile(img.ravel(), contrast_limits[1])
                normalized_data = (img - lower_clim) / (upper_clim - lower_clim)

        if isinstance(contrast_limits, list):
            lower_clim = contrast_limits[i][0]
            upper_clim = contrast_limits[i][1]
            normalized_data = (img - lower_clim) / (upper_clim - lower_clim)

        clims_used.append((lower_clim, upper_clim))
        colormapped_data = layer.colormap.map(normalized_data.flatten())
        colormapped_data = colormapped_data.reshape(normalized_data.shape + (4,))
        colormapped_list.append(colormapped_data)
        blended = blended + colormapped_data

    blended[..., 3] = 1

    colormapped_list.append(blended)
    return colormapped_list, clims_used


def create_matplotlib_figure(
    viewer, image_titles, row_titles, index, defined_clims=None, **kwargs
):
    title_list = [title + ("composite",) for title in image_titles]
    days_of_stainings = viewer.layers[0].data.shape[0]

    fig, ax = plt.subplots(
        nrows=days_of_stainings, ncols=len(viewer.layers) + 1, figsize=(8, 10)
    )
    clim_list = list()

    for day in range(days_of_stainings):
        if defined_clims is None:
            img_list, clims = blended_img(viewer, (day,) + index, **kwargs)
        else:
            img_list, clims = blended_img(
                viewer, (day,) + index, contrast_limits=defined_clims[day], **kwargs
            )
        clim_list.append(clims)

        for i, img in enumerate(img_list):
            ax[day, i].imshow(img)
            ax[day, i].xaxis.set_visible(False)
            plt.setp(ax[day, i].spines.values(), visible=False)
            ax[day, i].tick_params(left=False, labelleft=False)
            if i == 0:
                ax[day, i].set_ylabel(f"{row_titles[day]}")
                ax[day, i].yaxis.label.set_color("white")
            ax[day, i].set_title(title_list[day][i])

    return fig, ax, clim_list


def create_matrix_zigzag_row(rowCount, colCount, dataList):
    mat = []
    for rows in range(rowCount):
        rowList = []
        if rows % 2 == 0:
            for cols in range(colCount):
                index = colCount * rows + cols
                print("even", index)
                rowList.append(dataList[index])
            mat.append(rowList)
        if rows % 2 == 1:
            for cols in range(colCount - 1, -1, -1):
                index = colCount * rows + cols
                print("odd", index)
                rowList.append(dataList[index])
            mat.append(rowList)
    return mat