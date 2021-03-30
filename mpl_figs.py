import matplotlib.pyplot as plt
import numpy as np
import napari

def blended_img(viewer):
    blended = np.zeros(viewer.layers[0].data.shape + (4,))
    for layer in viewer.layers:
        # normalize data by clims
        normalized_data = (layer.data - layer.contrast_limits[0]) / (
        layer.contrast_limits[1] - layer.contrast_limits[0]
    )
        colormapped_data = layer.colormap.map(normalized_data.flatten())
        colormapped_data = colormapped_data.reshape(normalized_data.shape + (4,))

        blended = blended + colormapped_data
    
    blended[..., 3] = 1

    return blended

def create_matplotlib_figure(viewer, index, title_list):
    fig, ax = plt.subplots(nrows=viewer.layers[0].data.shape, ncols=len(viewer.layers), figsize=(12, 15))

    for i, (layer, title_list) in enumerate(zip(viewer.layers, title_list)):
        for ii in range(layer.data.shape[0]):
            img = layer.data[ii, index[0], index[1], index[2], :, :].compute()
            ax[i, ii].imshow(
                img,
                vmin=np.percentile(img.ravel(), 2),
                vmax=np.percentile(img.ravel(), 99.5), cmap='blue'
            )
            ax[i, ii].axis("off")
            ax[i, ii].set_title(title_list[ii])
    ax[0, 3].axis("off")
    ax[1, 3].axis("off")
    ax[2, 3].axis("off")
    plt.tight_layout()
#     fig.suptitle('Day 3 - BMP (50 ng/ml)', y=14)
#   # fig.savefig(save_path, dpi=300)
