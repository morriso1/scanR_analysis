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


def spiral_left(width, height):
    NORTH, S, W, E = (0, -1), (0, 1), (-1, 0), (1, 0)  # directions
    turn_left = {NORTH: W, W: S, S: E, E: NORTH}
    if width < 1 or height < 1:
        raise ValueError
    x, y = width // 2, height // 2  # start near the center
    dx, dy = NORTH  # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    while True:
        matrix[y][x] = count  # visit
        count += 1
        # try to turn left
        new_dx, new_dy = turn_left[dx, dy]
        new_x, new_y = x + new_dx, y + new_dy
        if (
            0 <= new_x < width and 0 <= new_y < height and matrix[new_y][new_x] is None
        ):  # can turn right
            x, y = new_x, new_y
            dx, dy = new_dx, new_dy
        else:  # try to move straight
            x, y = x + dx, y + dy
            if not (0 <= x < width and 0 <= y < height):
                return matrix  # nowhere to go


def spiral_right(width, height):
    NORTH, S, W, E = (0, -1), (0, 1), (-1, 0), (1, 0)  # directions
    turn_right = {NORTH: E, E: S, S: W, W: NORTH}  # old -> new direction
    if width < 1 or height < 1:
        raise ValueError
    x, y = width // 2, height // 2  # start near the center
    dx, dy = NORTH  # initial direction
    matrix = [[None] * width for _ in range(height)]
    count = 0
    while True:
        matrix[y][x] = count  # visit
        count += 1
        # try to turn right
        new_dx, new_dy = turn_right[dx, dy]
        new_x, new_y = x + new_dx, y + new_dy
        if (
            0 <= new_x < width and 0 <= new_y < height and matrix[new_y][new_x] is None
        ):  # can turn right
            x, y = new_x, new_y
            dx, dy = new_dx, new_dy
        else:  # try to move straight
            x, y = x + dx, y + dy
            if not (0 <= x < width and 0 <= y < height):
                return matrix  # nowhere to go