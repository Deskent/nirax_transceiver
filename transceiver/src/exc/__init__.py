from src.exc.exceptions import (
    AuthorizationError, ServerDataError, TestConnectionError, DataRequestError,
    CustomerNotFoundError, LicenseExpiredError, MethodNotFoundError, SettingsNotFoundError,
    ApiRequestError
)

CUSTOMER_EXCEPTIONS: tuple = (
    AuthorizationError,
    CustomerNotFoundError,
    DataRequestError,
    ServerDataError,
    TestConnectionError,
    LicenseExpiredError,
    MethodNotFoundError,
    SettingsNotFoundError,
)
