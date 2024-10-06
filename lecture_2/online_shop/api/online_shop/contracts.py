from __future__ import annotations

from lecture_2.online_shop.store.models import (
    CartEntity,
    ItemEntity,
    ItemInCartInfo,
    ItemInfo,
    PatchedItemInfo,
)
from pydantic import BaseModel, ConfigDict, NonNegativeFloat


class ItemResponse(BaseModel):
    id: int
    name: str
    price: NonNegativeFloat
    deleted: bool

    @staticmethod
    def from_entity(entity: ItemEntity) -> ItemResponse:
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
            deleted=entity.info.deleted,
        )


class ItemRequest(BaseModel):
    name: str
    price: NonNegativeFloat
    deleted: bool = False

    def as_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price, deleted=self.deleted)


class PatchedItemRequest(BaseModel):
    name: str | None = None
    price: NonNegativeFloat | None = None

    model_config = ConfigDict(extra="forbid")

    def as_patched_info(self) -> PatchedItemInfo:
        return PatchedItemInfo(name=self.name, price=self.price)


class CartResponse(BaseModel):
    id: int
    items: dict[int, ItemInCartInfo] = {}
    price: NonNegativeFloat

    @staticmethod
    def from_entity(entity: CartEntity) -> CartResponse:
        return CartResponse(
            id=entity.id, items=entity.info.items, price=entity.info.total_price
        )
