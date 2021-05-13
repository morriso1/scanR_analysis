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


def spiral_ccw(A):
    import numpy as np

    A = np.array(A)
    out = np.empty(0, dtype=np.int8)
    while A.size:
        out = np.concatenate((out, A[:, -1]))
        A = A[
            :,
            :-1,
        ].T[::-1]
    return out


def base_spiral(nrow, ncol):
    import numpy as np

    return spiral_ccw(np.arange(nrow * ncol).reshape(nrow, ncol))[::-1]


def to_spiral(nrow, ncol):
    import numpy as np

    A = np.arange(nrow * ncol).reshape(nrow, ncol)
    B = np.empty_like(A)
    B.flat[base_spiral(*A.shape)] = A.flat
    return B