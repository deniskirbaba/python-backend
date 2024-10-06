from typing import Iterable

from lecture_2.online_shop.store.models import (
    CartEntity,
    CartInfo,
    ItemEntity,
    ItemInCartInfo,
    ItemInfo,
    PatchedItemInfo,
)

_items = dict[int, ItemInfo]()
_carts = dict[int, CartInfo]()


def int_id_generator() -> Iterable[int]:
    id = 0
    while True:
        yield id
        id += 1


_items_id_generator = int_id_generator()
_carts_id_generator = int_id_generator()


def add_item(info: ItemInfo) -> ItemEntity:
    id = next(_items_id_generator)
    _items[id] = info
    return ItemEntity(id=id, info=info)


def delete_item(id: int) -> None:
    if id in _items:
        _items[id].deleted = True


def get_item(id: int) -> ItemEntity | None:
    if id not in _items:
        return None
    return ItemEntity(id=id, info=_items[id])


def get_items_list(
    offset: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    show_deleted: bool = False,
) -> Iterable[ItemEntity]:
    curr = 0
    for id, info in _items.items():
        if (
            (offset <= curr < offset + limit)
            and (show_deleted or not info.deleted)
            and (min_price is None or info.price >= min_price)
            and (max_price is None or info.price <= max_price)
        ):
            yield ItemEntity(id=id, info=info)

        curr += 1


def put_item(id: int, info: ItemInfo) -> ItemEntity | None:
    if id not in _items:
        return None
    _items[id] = info
    return ItemEntity(id=id, info=info)


def patch_item(id: int, info: PatchedItemInfo) -> ItemEntity | None:
    if id not in _items:
        return None

    if info.name is not None:
        _items[id].name = info.name

    if info.price is not None:
        _items[id].price = info.price

    return ItemEntity(id=id, info=_items[id])


def create_cart() -> int:
    id = next(_carts_id_generator)
    _carts[id] = CartInfo()
    return id


def get_cart(id: int) -> CartEntity | None:
    if id not in _carts:
        return None
    return CartEntity(id=id, info=_carts[id])


def get_carts_list(
    offset: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    min_quantity: int | None = None,
    max_quantity: int | None = None,
) -> Iterable[CartEntity]:
    curr = 0
    for id, info in _carts.items():
        if (
            (offset <= curr < offset + limit)
            and (min_price is None or info.total_price >= min_price)
            and (max_price is None or info.total_price <= max_price)
            and (min_quantity is None or info.total_quantity >= min_quantity)
            and (max_quantity is None or info.total_quantity <= max_quantity)
        ):
            yield CartEntity(id=id, info=info)

        curr += 1


def add_item_in_cart(cart_id: int, item_id: int) -> CartEntity | None:
    if not (cart_id in _carts and item_id in _items):
        return None

    if item_id not in _carts[cart_id].items:
        _carts[cart_id].items[item_id] = ItemInCartInfo(
            info=_items[item_id], quantity=1
        )
    else:
        _carts[cart_id].items[item_id].quantity += 1

    return CartEntity(id=cart_id, info=_carts[cart_id])
