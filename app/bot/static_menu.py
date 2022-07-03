from collections import namedtuple


MenuElement = namedtuple('MenuElement', ['name', 'action', 'content'])

admin_menu = MenuElement(name='Меню', action='navigation', content=(
    MenuElement(name='Получить данные', action='get_prepared', content=()),
    MenuElement(name='Форматировать заказ', action='format', content=()),
))
