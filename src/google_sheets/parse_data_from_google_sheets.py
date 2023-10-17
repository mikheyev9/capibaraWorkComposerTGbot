from pydantic import BaseModel, Field


class ValuesData(BaseModel):
    row: str
    project: str = Field(None)
    create_project: str = Field(None)
    parsing: str = Field(None)
    verstka: str = Field(None)
    buy_domain: str = Field(None)
    deploy: str = Field(None)
    content: str = Field(None)
    acquiring: str = Field(None)
    release: str = Field(None)


class JsonGoogleSheets(BaseModel):
    row_or_column: str
    range_: str
    values: list[ValuesData]


async def parse_all_read_data(response: dict) -> JsonGoogleSheets:
    try:
        values = []
        row = 1
        for value in response['values']:
            row += 1
            if len(value) > 0:
                value = ValuesData(
                    row=row,
                    project=value[0],
                    create_project=value[1] if len(value) > 1 else None,
                    parsing=value[2] if len(value) > 2 else None,
                    verstka=value[3] if len(value) > 3 else None,
                    buy_domain=value[4] if len(value) > 4 else None,
                    deploy=value[5] if len(value) > 5 else None,
                    content=value[6] if len(value) > 6 else None,
                    acquiring=value[7] if len(value) > 7 else None,
                    release=value[8] if len(value) > 8 else None,
                )
                values.append(value)
        response_data = JsonGoogleSheets(
            row_or_column=response['majorDimension'],
            range_=response['range'],
            values=values,
        )
        return response_data
    except KeyError:
        return []


class JsonGoogleSheetsRows(BaseModel):
    row_or_column: str
    range_: str
    values: list[tuple[str, str]]


async def parse_data_rows(response: dict) -> JsonGoogleSheetsRows:
    try:
        values = []
        row = 1
        for value in response['values']:
            row += 1
            if len(value) > 0:
                values.append((row, value[0]))
        response_data = JsonGoogleSheetsRows(
            row_or_column=response['majorDimension'],
            range_=response['range'],
            values=values,
        )
        return response_data
    except KeyError:
        return []
