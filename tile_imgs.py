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


def spiral_cw(A):
    import numpy as np

    A = np.array(A)
    out = []
    while A.size:
        out.append(A[:, 0])  # take first column
        A = A[:, 1:].T[:, ::-1]  # cut off first column and rotate counterclockwise
    return np.concatenate(out)


def base_spiral(nrow, ncol):
    import numpy as np

    return spiral_cw(np.arange(nrow * ncol).reshape(nrow, ncol))[::-1]


def to_spiral(nrows, ncols):
    import numpy as np

    A = np.arange(nrows * ncols).reshape(nrows, ncols)
    B = np.empty_like(A)
    B.flat[base_spiral(*A.shape)] = A.flat
    return np.flip(B, axis=1)