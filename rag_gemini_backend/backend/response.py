from rest_framework.response import Response
from rest_framework import status


class CustomResponse(Response):
    def __init__(
        self,
        data=None,
        status_code=status.HTTP_200_OK,
        message="",
        success="success",
        **kwargs,
    ):
        response_data = {"status": success, "message": message, "data": data}
        super().__init__(data=response_data, status=status_code, **kwargs)

    @classmethod
    def success(
        cls, data=None, message="Success", status_code=status.HTTP_200_OK, **kwargs
    ):
        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success="success",
            **kwargs,
        )

    @classmethod
    def created(cls, data=None, message="Created", **kwargs):
        return cls(
            data=data,
            status_code=status.HTTP_201_CREATED,
            message=message,
            success="success",
            **kwargs,
        )

    @classmethod
    def error(
        cls,
        data=None,
        message="Error",
        status_code=status.HTTP_400_BAD_REQUEST,
        **kwargs,
    ):
        return cls(
            data=data,
            status_code=status_code,
            message=message,
            success="error",
            **kwargs,
        )
