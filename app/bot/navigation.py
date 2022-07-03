from collections import deque, namedtuple

from bot.static_menu import admin_menu


def encode_path(path: deque, structure: namedtuple) -> list:
    path = path.copy()
    result = []
    while len(path) > 0:
        key = path.pop()
        content_list = [elem.name for elem in structure.content]
        idx = content_list.index(key)
        result.append(idx)
        structure = structure.content[idx]
        if structure is None:
            break
    return result


def decode_path(path: list, structure: namedtuple) -> deque:
    result = deque([])
    for idx in path:
        content_list = [elem.name for elem in structure.content]
        key = content_list[idx]
        result.appendleft(key)
        structure = structure.content[idx]
        if structure is None:
            break
    return result


def get_element_from_path(path: list, structure: namedtuple) -> namedtuple:
    path = path.copy()
    if len(path) == 0:
        return structure

    for idx in path:
        structure = structure.content[idx]
    return structure


if __name__ == '__main__':
    path_queue = deque(['Форматировать'])
    for elem_ in admin_menu.content:
        idx_ = admin_menu.content.index(elem_)
    path_encoded = encode_path(path_queue, admin_menu)
    path_decoded = decode_path(path_encoded, admin_menu)
    print(get_element_from_path(path_encoded, admin_menu))
