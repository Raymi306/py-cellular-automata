def get_nw(board, index):
    default_case = index - board.max_x_pos - 1

    if index < board.max_x_pos\
            and index % board.max_x_pos != 0:  # top row exclude top left
        return default_case + board.total_cells
    elif index % board.max_x_pos == 0:  # left col
        left_col_case = index - 1
        if left_col_case < 0:  # top left...
            return board.total_cells - 1
        else:
            return left_col_case
    else:
        return default_case


def get_ne(board, index):
    default_case = index - board.max_x_pos + 1
    # exclude corner
    if index < board.max_x_pos\
            and index % board.max_x_pos != board.max_x_pos - 1:
        return default_case + board.total_cells
    elif index % board.max_x_pos == board.max_x_pos - 1:
        right_col_case = default_case - board.max_x_pos
        if right_col_case < 0:
            return board.total_cells + right_col_case
        else:
            return right_col_case
    else:
        return default_case


def get_sw(board, index):
    default_case = index + board.max_x_pos - 1
    # bot row exclude bot left
    if index + board.max_x_pos >= board.total_cells\
            and index % board.max_x_pos != 0:
        return default_case - board.total_cells
    elif index % board.max_x_pos == 0:  # left col
        left_col_case = default_case + board.max_x_pos
        if left_col_case >= board.total_cells:
            return board.max_x_pos - 1
        else:
            return left_col_case
    else:
        return default_case


def get_se(board, index):
    default_case = index + board.max_x_pos + 1

    # bot row exclude bot right
    if index + board.max_x_pos >= board.total_cells\
            and index % board.max_x_pos != board.max_x_pos - 1:
        return default_case - board.total_cells
    elif index % board.max_x_pos == board.max_x_pos - 1:  # right col
        right_col_case = default_case - board.max_x_pos
        if right_col_case >= board.total_cells:
            return 0
        else:
            return right_col_case
    else:
        return default_case


def get_n(board, index):
    if index >= board.max_x_pos:
        return index - board.max_x_pos
    else:
        return index + board.total_cells - board.max_x_pos


def get_w(board, index):
    if index - 1 >= 0\
            and (index - 1) % board.max_x_pos != board.max_x_pos - 1:
        return index - 1
    else:
        return index + board.max_x_pos - 1


def get_e(board, index):
    if (index + 1) % board.max_x_pos != 0\
       and index + 1 < board.total_cells:
        return index + 1
    else:
        return index - board.max_x_pos + 1


def get_s(board, index):
    if (index + board.max_x_pos) < board.total_cells:
        return index + board.max_x_pos
    else:
        return index - board.total_cells + board.max_x_pos


functions = (
        get_nw, get_n, get_ne, get_w, get_e, get_sw, get_s, get_se
        )
