# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Callable, NamedTuple, Union

from submodules.fastapi_haljson.src.halresponse import (
    HALJSONResponse,
    NotFoundResponse,
    OkResponse,
    UnprocessableEntityResponse,
)


class ResponseToJSONBody(NamedTuple):
    converters: dict[
        str,
        Union[
            Callable[[Any], OkResponse],
            Callable[[Any], NotFoundResponse],
            Callable[[Any], UnprocessableEntityResponse],
        ],
    ]

    @classmethod
    def from_response_names(
        cls, to_ok: list[str], to_not_found: list[str], to_unprocessable_entity: list[str]
    ) -> ResponseToJSONBody:
        return ResponseToJSONBody(
            {
                **{name: (lambda dto: OkResponse.from_response_data(dto)) for name in to_ok},
                **{name: (lambda dto: NotFoundResponse.from_response_data(dto)) for name in to_not_found},
                **{
                    name: (lambda dto: UnprocessableEntityResponse.from_response_data(dto))
                    for name in to_unprocessable_entity
                },
            }
        )

    def convert(self, dto) -> HALJSONResponse:
        print(type(dto).__name__)
        return self.converters[type(dto).__name__](dto)
