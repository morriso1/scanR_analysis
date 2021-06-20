import numpy as np
from skimage import io
from dask import delayed
import dask.array as da
from dask_image.imread import imread
import pandas as pd
import os
from glob import glob


def determine_tif_structure(glob_pat, channel_names=None, elution_control_regex=r"EL"):

    if channel_names == None:
        channel_names = ["DAPI", "GFP", "mCherry2", "Alexa 647"]
    filenames = sorted(glob(os.path.join(glob_pat)))
    df_filenames = pd.DataFrame({"file_paths": filenames})
    df_filenames["day_index"] = (
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

    num_unique = df_filenames.groupby("day_index").nunique()["well"][0]
    unique_wells = df_filenames["well"].unique()
    exchange_list = list(range(num_unique)) * (df_filenames["day_index"].nunique() + 1)
    exchange_list = exchange_list[: len(unique_wells)]
    df_filenames["w_index"] = df_filenames["well"].replace(
        unique_wells,
        exchange_list,
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
    df_filenames["stained_every_round"] = np.invert(
        df_filenames["file_paths"].str.contains(elution_control_regex)
    )
    return df_filenames


def determine_tif_structure_with_genotype(glob_pat, genotypes, channel_names=None):

    if channel_names == None:
        channel_names = ["DAPI", "GFP", "mCherry2", "Alexa 647"]
    filenames = sorted(glob(os.path.join(glob_pat)))
    df_filenames = pd.DataFrame({"file_paths": filenames})

    geno_str = r"|".join(genotypes)
    geno_str = f"({geno_str})"

    df_filenames["genotype"] = df_filenames["file_paths"].str.extract(
        geno_str, expand=False
    )

    df_filenames["genotype_index"] = df_filenames["genotype"].copy()
    for i, geno in enumerate(genotypes):
        condition = df_filenames["genotype"] == geno
        df_filenames["genotype_index"][condition] = i

    df_filenames["day_index"] = (
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
    num_unique = df_filenames.groupby(["genotype", "day_index"]).nunique()["well"][0]
    df_filenames["w_index"] = df_filenames["well"].replace(
        df_filenames["well"].unique(),
        list(range(num_unique)) * df_filenames["day_index"].nunique() * len(genotypes),
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


def lazy_read_multichannel_img(
    dir_path,
    glob_for_each_channel=("*DAPI*.tif", "*GFP*.tif", "*mCherry*", "*647*.tif"),
):
    imgs = da.stack(
        [imread(os.path.join(dir_path, globs)) for globs in glob_for_each_channel]
    )
    return imgs


def reading_in_tifs_lazy_to_multidimensional(df_filenames, indexes):
    # [1,1] is for the x and y axis
    arrays = np.empty(
        tuple(df_filenames.nunique()[indexes].tolist() + [1, 1]),
        dtype="object",
    )

    for row in df_filenames.iterrows():
        lazy_array = delayed(io.imread)(row[1]["file_paths"])

        row_indexes = [row[1][index] for index in indexes]
        row_indexes = row_indexes + [0, 0]
        row_indexes = tuple(row_indexes)

        arrays[row_indexes] = da.from_delayed(
            lazy_array, shape=(2048, 2048), dtype="uint16"
        )

    dask_array = da.block(arrays.tolist())
    return dask_array