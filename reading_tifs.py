def determine_tif_structure(glob_pat, channel_names=None):
    import pandas as pd
    import os
    from glob import glob
    
    if channel_names == None:
        channel_names = ["DAPI", "GFP", "mCherry2", "A647"]
    filenames = sorted(glob(os.path.join(glob_pat)))
    df_filenames = pd.DataFrame({"file_paths": filenames})
    df_filenames["day"] = (
        df_filenames["file_paths"]
        .str.extract(r"(Day\d)", expand=False)
        .str.extract(r"(\d)")
        .astype(int)
    )
    df_filenames["well"] = (
        df_filenames["file_paths"]
        .str.extract(r"(W\d{5})", expand=False)
        .str.extract(r"(\d{5})")
        .astype(int)
    )
    num_unique = df_filenames.groupby("day").nunique()["well"][0]
    df_filenames["w_index"] = df_filenames["well"].replace(
        df_filenames["well"].unique(),
        list(range(num_unique)) * df_filenames["day"].nunique(),
    )

    df_filenames["p_index"] = (
        df_filenames["file_paths"]
        .str.extract(r"(P\d{5})", expand=False)
        .str.extract("(\d{5})")
        .astype(int)
    ) - 1

    df_filenames["z_index"] = (
        df_filenames["file_paths"]
        .str.extract(r"(Z\d{5})", expand=False)
        .str.extract("(\d{5})")
        .astype(int)
    )

    df_filenames["t_index"] = (
        df_filenames["file_paths"]
        .str.extract(r"(T\d{5})", expand=False)
        .str.extract("(\d{5})")
        .astype(int)
    )

    df_filenames["channel"] = (
        df_filenames["file_paths"]
        .str.split("--", expand=True)
        .iloc[:, -1]
        .str.strip(".tif")
    )

    df_filenames["c_index"] = df_filenames["channel"].replace(
        channel_names, list(range(len(channel_names)))
    )

    return df_filenames

def reading_in_tifs_not_lazy(glob_pat, channel_names=None):
    import numpy as np
    from skimage import io

    df_filenames = determine_tif_structure(glob_pat, channel_names=channel_names)
    arrays = np.empty(
        df_filenames.nunique()[
            ["c_index", "day", "w_index", "p_index", "t_index", "z_index"]
        ].tolist()
        + [2048, 2048],
        dtype='uint16',
    )
    for row in df_filenames.iterrows():
        arrays[
            row[1]["c_index"],
            row[1]["day"],
            row[1]["w_index"],
            row[1]["p_index"],
            row[1]["t_index"],
            row[1]["z_index"],
            :,
            :,
        ] = io.imread(row[1]['file_paths'])
    
    return arrays

def reading_in_tifs_lazy(glob_pat, channel_names=None):
    import numpy as np
    from skimage import io
    from dask import delayed
    import dask.array as da

    df_filenames = determine_tif_structure(glob_pat, channel_names=channel_names)
    # [1,1] is for the x and y axis
    arrays = np.empty(
        df_filenames.nunique()[
            ["c_index", "day", "w_index", "p_index"]
        ].tolist()
        + [1, 1],
        dtype='object',
    )
    for row in df_filenames.iterrows():
        lazy_array = delayed(io.imread)(
            row[1]['file_paths']
        )

        arrays[
            row[1]["c_index"],
            row[1]["day"],
            row[1]["w_index"],
            row[1]["p_index"],
            0,
            0,
        ] = da.from_delayed(lazy_array, shape=(2048, 2048), dtype="uint16")
    
    dask_array = da.block(arrays.tolist())
    return dask_array