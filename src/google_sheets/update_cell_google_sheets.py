from google_sheets.auth_and_permissions import service_google_sheets
from settings.config import GRAY_COLOR, GREEN_COLOR, ORANGE_COLOR, SPREAD_SHEET_ID

sheetId = '1065963106'


async def update_color_in_cell(
    service,
    sheetId: str,
    row_start: int,
    row_end: int,
    column_start: int,
    column_end: int,
    color: str
):
    body = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": row_start,
                        "endRowIndex": row_end,
                        "startColumnIndex": column_start,
                        "endColumnIndex": column_end
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredFormat": {
                                        "backgroundColor": color
                                    }
                                }
                            ]
                        }
                    ],
                    "fields": "userEnteredFormat.backgroundColor"
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREAD_SHEET_ID,
        body=body
    ).execute()


async def update_after_project(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 1, 2, GRAY_COLOR
    )
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row), int(row)+1, 2, 3, GRAY_COLOR
    )


async def update_color_correction_create_project(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 1, 2, ORANGE_COLOR
    )


async def update_color_create_project(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 1, 2, ORANGE_COLOR
    )


async def update_color_correction_after_create_project(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 1, 2, GREEN_COLOR
    )


async def update_color_after_create_project(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 1, 2, GREEN_COLOR
    )
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 3, 4, GRAY_COLOR
    )
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 4, 5, GRAY_COLOR
    )


async def update_color_correction_parsing(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row), int(row)+1, 2, 3, ORANGE_COLOR
    )


async def update_color_parsing(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row), int(row)+1, 2, 3, ORANGE_COLOR
    )


async def update_color_correction_after_parsing(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row), int(row)+1, 2, 3, GREEN_COLOR
    )


async def update_color_after_parsing(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row), int(row)+1, 2, 3, GREEN_COLOR
    )


async def update_color_correction_frontend(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 3, 4, ORANGE_COLOR
    )


async def update_color_frontend(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 3, 4, ORANGE_COLOR
    )


async def update_color_correction_after_frontend(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 3, 4, GREEN_COLOR
    )


async def update_color_after_frontend(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 3, 4, GREEN_COLOR
    )


async def update_after_buy_domain(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 4, 5, GREEN_COLOR
    )


async def update_after_buy_domain_and_frontend(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 5, 6, GRAY_COLOR
    )


async def update_color_correction_deploy(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 5, 6, ORANGE_COLOR
    )


async def update_color_deploy(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 5, 6, ORANGE_COLOR
    )


async def update_color_correction_after_deploy(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 5, 6, GREEN_COLOR
    )


async def update_color_after_deploy(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 5, 6, GREEN_COLOR
    )


async def update_color_after_deploy_and_parsing(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 6, 7, GRAY_COLOR
    )


async def update_after_content(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 7, 8, GRAY_COLOR
    )


async def update_color_correction_acquiring(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 7, 8, ORANGE_COLOR
    )


async def update_color_acquiring(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 7, 8, ORANGE_COLOR
    )


async def update_color_correction_after_acquiring(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 7, 8, GREEN_COLOR
    )


async def update_color_after_acquiring(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 7, 8, GREEN_COLOR
    )
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 8, 9, GRAY_COLOR
    )


async def update_color_release(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 8, 9, ORANGE_COLOR
    )


async def update_color_after_release(row):
    await update_color_in_cell(
        service_google_sheets, sheetId,
        int(row)-1, int(row)+1, 8, 9, GREEN_COLOR
    )


async def update_text_in_cell(range_cell, text):
    request_body = {
        'majorDimension': 'ROWS',
        'values': [[text]]
    }
    service_google_sheets.spreadsheets().values().update(
        spreadsheetId=SPREAD_SHEET_ID,
        range=range_cell,
        valueInputOption='USER_ENTERED',
        body=request_body
    ).execute()
