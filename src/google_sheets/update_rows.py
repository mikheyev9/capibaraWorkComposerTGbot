from crud.read_data_db import get_projects_site_in_db
from crud.update_data_db import update_projects_site
from google_sheets.auth_and_permissions import service_google_sheets
from google_sheets.get_cell_google_sheets import spreadsheet_read_all_values
from google_sheets.parse_data_from_google_sheets import parse_data_rows


async def update_rows_for_projects_sites():
    response = await spreadsheet_read_all_values(service_google_sheets, 'A')
    json_google_sheets_data_rows = await parse_data_rows(response)

    try:
        values_list = json_google_sheets_data_rows.values
    except AttributeError:
        return

    for value in values_list:
        row = value[0]
        project_name = value[1]

        project_site = await get_projects_site_in_db(project_name)

        if project_site is not None and row != project_site.row:
            project_site_data = project_site.__dict__
            project_site_data['row'] = row
            await update_projects_site(project_site.id, project_site_data)
