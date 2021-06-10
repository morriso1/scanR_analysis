from scanR_analysis import tile_imgs
import dask.array as da


def get_img_frame(
    img,
    df,
    day_index=0,
    w_index=0,
    p_index=None,
):
    if p_index is None:
        indexes = df.query(
            "day_index == @day_index & w_index == @w_index & stained_every_round == True"
        ).index.tolist()
        img = img[:, indexes, ...]
        img = da.block([[img[:, i, ...] for i in x] for x in tile_imgs.to_spiral(6, 6)])
    else:
        indexes = df.query(
            "day_index == @day_index & w_index == @w_index & p_index == @p_index & stained_every_round == True"
        ).index.tolist()
        img = img[:, indexes, ...]

    return img


def get_lab_frame(
    img,
    df,
    day_index=0,
    w_index=0,
    p_index=None,
):
    if p_index is None:
        indexes = df.query(
            "day_index == @day_index & w_index == @w_index & stained_every_round == True"
        ).index.tolist()
        img = img[indexes, ...]
        img = da.block([[img[i, ...] for i in x] for x in tile_imgs.to_spiral(6, 6)])
    else:
        indexes = df.query(
            "day_index == @day_index & w_index == @w_index & p_index == @p_index & stained_every_round == True"
        ).index.tolist()
        img = img[indexes, ...]

    return img


def get_specific_well(img, df, well, p_index=None):
    if p_index is None:
        indexes = df.query("well == @well").index.tolist()
        img = img[:, indexes, ...]
        img = da.block([[img[i, ...] for i in x] for x in tile_imgs.to_spiral(6, 6)])
    else:
        indexes = df.query("well == @well & p_index == @p_index").index.tolist()
        img = img[:, indexes, ...]

    return img