def entry_int_checker(new_val):
    try:
        int(new_val)
        return True
    except ValueError:
        return False


def clamp_int(num, left, right):
    if num < left:
        return left
    if num > right:
        return right
    return num
