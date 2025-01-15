from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONE_NUMBER = "This phone number is incorrect. Please try again."
    USER_DOES_NOT_EXIST = "This user does not exist"
    CATEGORY_DOES_NOT_EXIST = "Category does not exist"
    START_DATE_IS_GREATER_THAN_END_DATE = "start_date cannot be later than end_date."
