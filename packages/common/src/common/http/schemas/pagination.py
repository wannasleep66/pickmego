from common.http.schemas.base import ResponseSchema


class PaginationMeta(ResponseSchema):
    page: int
    page_size: int
    total: int


class PaginatedResponse[T](ResponseSchema):
   data: list[T]
   meta: PaginationMeta
