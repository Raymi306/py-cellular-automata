def get_nw(board, index):
    return index - board.max_x_pos - 1


def get_ne(board, index):
    return index - board.max_x_pos + 1


def get_sw(board, index):
    return index + board.max_x_pos - 1


def get_se(board, index):
    return index + board.max_x_pos + 1


def get_n(board, index):
    return index - board.max_x_pos


def get_w(_, index):
    return index - 1


def get_e(_, index):
    return index + 1


def get_s(board, index):
    return index + board.max_x_pos


functions = (
        get_nw, get_n, get_ne, get_w, get_e, get_sw, get_s, get_se
        )
