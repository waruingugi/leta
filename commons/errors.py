from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONE_NUMBER = "This phone number is incorrect. Please try again."
    USER_DOES_NOT_EXIST = "This user does not exist"
