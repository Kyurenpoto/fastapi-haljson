# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class HALJSONResponse(JSONResponse):
    media_type = "application/hal+json"


class OkResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> OkResponse:
        return OkResponse(content=jsonable_encoder(data))


class NotFoundResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> NotFoundResponse:
        return NotFoundResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(data))


class UnprocessableEntityResponse(HALJSONResponse):
    @classmethod
    def from_response_data(cls, data) -> UnprocessableEntityResponse:
        return UnprocessableEntityResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(data)
        )