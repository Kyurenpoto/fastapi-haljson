# SPDX-FileCopyrightText: © 2021 Kyurenpoto <heal9179@gmail.com>

# SPDX-License-Identifier: MIT

from __future__ import annotations

from pydantic import BaseModel
from pydantic.fields import Field


class HALLink(BaseModel):
    href: str = Field(
        ...,
        description="HATEOAS link",
    )

    @classmethod
    def doc_link(cls, rel: str, api: str, http_method: str, profile_location: str) -> HALLink:
        return HALLink(href=profile_location + "_".join([rel] + api.split("/")[1:] + [http_method]))


class HALBase(BaseModel):
    links: dict[str, HALLink] = Field(
        ...,
        description="HATEOAS links",
    )

    @classmethod
    def from_apis(cls, routes: dict[str, str]) -> HALBase:
        return HALBase(links={rel: HALLink(href=api) for rel, api in routes.items()})

    @classmethod
    def from_apis_with_requested(cls, routes: dict[str, str], requested: str, http_method) -> HALBase:
        return HALBase(
            links={
                "self": HALLink(href=routes[requested]),
                "profile": HALLink.doc_link(requested, routes[requested], http_method, "/docs#default/"),
                "profile2": HALLink.doc_link(requested, routes[requested], http_method, "/redoc#operation/"),
                **HALBase.from_apis(routes).links,
            }
        )
