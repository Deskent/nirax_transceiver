from fastapi import HTTPException, status


class CustomException(HTTPException):

    def with_message(self, text: str):
        self.detail = text

        return self


AuthorizationDenied = CustomException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Wrong login or password"
)

ApiRequestError = CustomException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Data not found"
)

ArticleNotFound = CustomException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Артикул не задан"
)

SuppliersNotFound = CustomException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Поставщики не заданы"
)

RequestDataError = CustomException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Ошибка входных данных"
)


class AuthorizationError(Exception):
    pass


class ServerDataError(Exception):
    pass


class TestConnectionError(Exception):
    pass


class DataRequestError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class MethodNotFoundError(Exception):
    pass


class SettingsNotFoundError(Exception):
    pass


class LicenseExpiredError(Exception):
    pass
