from sisense_utils.models.sisense import DashboardSummary, Folder


def _find_folder_components(
    folder_struct: Folder, dashboard_oid: str, folder_components: list[str]
) -> list[str] | None:
    folder_components.append(folder_struct.name)

    if folder_struct.dashboards is not None:
        for dashboard in folder_struct.dashboards:
            if dashboard.oid == dashboard_oid:
                return folder_components

    if not folder_struct.folders:
        return None

    for folder_to_search in folder_struct.folders:
        paths = _find_folder_components(folder_to_search, dashboard_oid, folder_components)
        if paths is not None:
            return paths

        folder_components.pop()

    return None


def get_folder_components(available_folders: Folder, dashboard: DashboardSummary) -> list[str]:
    result = _find_folder_components(available_folders, dashboard.oid, [])
    if not result:
        raise Exception(f"Dashboard with oid {dashboard.oid} not found in folder structure")

    if result[0] == "rootFolder":
        return result[1:]

    raise Exception("Unexpected folder structure")
