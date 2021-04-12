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