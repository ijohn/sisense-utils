from __future__ import annotations

from datetime import datetime

from sisense_utils.models.api_model import APIModel


class ParentFolder(APIModel):
    oid: str
    name: str | None = None
    parent_id: str | None = None


class Share(APIModel):
    share_id: str
    type: str
    subscribe: bool | None = None
    rule: str | None = None


class BaseDashboard(APIModel):
    title: str
    oid: str
    last_publish: datetime | None = None


class DashboardSummary(BaseDashboard):
    parent_folder: ParentFolder | None = None


class Dashboard(BaseDashboard):
    parent_folder: str | None = None
    shares: list[Share]


class Folder(APIModel):
    name: str
    oid: str | None = None
    parent_id: str | None = None
    folders: list[Folder] | None = None
    dashboards: list[Dashboard] | None = None


Folder.update_forward_refs()
