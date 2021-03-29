def blended_img(viewer):
    import napari
    import numpy as np
    
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
