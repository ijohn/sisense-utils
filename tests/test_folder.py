from typing import Any

import pytest

from sisense_utils.folder import get_folder_components
from sisense_utils.models.sisense import DashboardSummary, Folder, ParentFolder


def test_get_folder_components() -> None:
    navver_response: dict[str, Any] = {
        "oid": None,
        "name": "rootFolder",
        "dashboards": [
            {"title": "Dashboard 1", "oid": "60325079939fb3002dac33b8", "parentFolder": None, "shares": []},
            {"title": "Dashboard 2", "oid": "60325079939fb3002dac33b9", "parentFolder": None, "shares": []},
        ],
        "folders": [
            {
                "oid": "61bf63774f8f42003700b317",
                "parentId": None,
                "name": "Test Folder",
                "dashboards": [
                    {
                        "title": "Dashboard 3",
                        "oid": "60325079939fb3002dac33bA",
                        "parentFolder": "61bf63774f8f42003700b317",
                        "shares": [],
                    }
                ],
            },
            {
                "oid": "61bf63774f8f42003700b318",
                "parentId": None,
                "name": "Another Folder",
                "dashboards": [],
                "folders": [
                    {
                        "oid": "61bf63774f8f42003700b319",
                        "name": "Child Folder",
                        "parentId": "61bf63774f8f42003700b318",
                        "dashboards": [
                            {
                                "title": "Dashboard 4",
                                "oid": "60325079939fb3002dac33bB",
                                "parentFolder": "61bf63774f8f42003700b319",
                                "shares": [],
                            }
                        ],
                        "folders": [
                            {
                                "oid": "61bf63774f8f42003700b320",
                                "name": "Grandchild Folder",
                                "parentId": "61bf63774f8f42003700b319",
                                "dashboards": [
                                    {
                                        "title": "Dashboard 5",
                                        "oid": "60325079939fb3002dac33bC",
                                        "parentFolder": "61bf63774f8f42003700b320",
                                        "shares": [],
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "oid": "61bf63774f8f42003700b324",
                        "name": "Sibling Child Folder",
                        "parentId": "61bf63774f8f42003700b318",
                        "dashboards": [
                            {
                                "title": "Dashboard 8",
                                "oid": "60325079939fb3002dac33bF",
                                "parentFolder": "61bf63774f8f42003700b324",
                                "shares": [],
                            }
                        ],
                    },
                ],
            },
            {
                "oid": "61bf63774f8f42003700b321",
                "parentId": None,
                "name": "Blank Folder",
            },
            {
                "oid": "61bf63774f8f42003700b322",
                "parentId": None,
                "name": "Secret Folder",
                "dashboards": [],
                "folders": [
                    {
                        "oid": "61bf63774f8f42003700b323",
                        "name": "Secret Child Folder",
                        "parentId": "61bf63774f8f42003700b322",
                        "dashboards": [
                            {
                                "title": "Dashboard 6",
                                "oid": "60325079939fb3002dac33bD",
                                "parentFolder": "61bf63774f8f42003700b323",
                                "shares": [],
                            }
                        ],
                    }
                ],
            },
        ],
    }
    available_folders = Folder.parse_obj(navver_response)

    assert (
        get_folder_components(
            available_folders, DashboardSummary(title="Dashboard 1", oid="60325079939fb3002dac33b8", parent_folder=None)
        )
        == []
    )
    assert (
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 3",
                oid="60325079939fb3002dac33bA",
                parent_folder=ParentFolder(oid="61bf63774f8f42003700b317", name="Test Folder", parent_id=None),
            ),
        )
        == ["Test Folder"]
    )
    assert (
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 4",
                oid="60325079939fb3002dac33bB",
                parent_folder=ParentFolder(
                    oid="61bf63774f8f42003700b319", name="Child Folder", parent_id="61bf63774f8f42003700b318"
                ),
            ),
        )
        == ["Another Folder", "Child Folder"]
    )
    assert (
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 5",
                oid="60325079939fb3002dac33bC",
                parent_folder=ParentFolder(
                    oid="61bf63774f8f42003700b320", name="Grandchild Folder", parent_id="61bf63774f8f42003700b319"
                ),
            ),
        )
        == ["Another Folder", "Child Folder", "Grandchild Folder"]
    )
    assert (
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 8",
                oid="60325079939fb3002dac33bF",
                parent_folder=ParentFolder(
                    oid="61bf63774f8f42003700b324", name="Sibling Child Folder", parent_id="61bf63774f8f42003700b318"
                ),
            ),
        )
        == ["Another Folder", "Sibling Child Folder"]
    )
    assert (
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 6",
                oid="60325079939fb3002dac33bD",
                parent_folder=ParentFolder(
                    oid="61bf63774f8f42003700b323", name="Secret Child Folder", parent_id="61bf63774f8f42003700b322"
                ),
            ),
        )
        == ["Secret Folder", "Secret Child Folder"]
    )

    with pytest.raises(Exception, match="Dashboard with oid 60325079939fb3002dac33b7 not found in folder structure"):
        get_folder_components(
            available_folders, DashboardSummary(title="Dashboard 0", oid="60325079939fb3002dac33b7", parent_folder=None)
        )

    with pytest.raises(Exception, match="Dashboard with oid 60325079939fb3002dac33bE not found in folder structure"):
        get_folder_components(
            available_folders,
            DashboardSummary(
                title="Dashboard 7",
                oid="60325079939fb3002dac33bE",
                parent_folder=ParentFolder(
                    oid="61bf63774f8f42003700b324", name="Sibling Child Folder", parent_id="61bf63774f8f42003700b318"
                ),
            ),
        )
