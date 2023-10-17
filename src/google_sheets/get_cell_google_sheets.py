from settings.config import SPREAD_SHEET_ID


async def spreadsheet_read_all_values(service, range_column: str) -> dict:
    request = service.spreadsheets().values().get(
        spreadsheetId=SPREAD_SHEET_ID,
        range=f'A2:{range_column}100',
    )
    response = request.execute()
    return response


async def spreadsheet_read_color_from_data(service, ranges: list[str]) -> dict:
    request = service.spreadsheets().get(
        spreadsheetId=SPREAD_SHEET_ID,
        ranges=ranges,
        includeGridData=True
    )
    response = request.execute()
    color_cell = response['sheets'][0]['data'][0]['rowData'][0]['values']
    color_cell = color_cell[0]['effectiveFormat']['backgroundColor']
    return color_cell
