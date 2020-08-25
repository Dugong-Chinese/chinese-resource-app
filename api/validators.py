"""Validators for use with the API to validate user input.
Validators return nothing and raise ValidationError if anything is invalid, with optional
extra information on the error in the exception's message.

To use, simply call the validator on the value and handle ValidationError in case of
input error.
"""

import re


class ValidationError(Exception):
    pass


# Regexes for emails borrowed from Django's email validator.
EMAIL_USER_PART = re.compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',
    re.IGNORECASE,
)
EMAIL_DOMAIN_PART = re.compile(
    r"((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z",
    re.IGNORECASE,
)


def validate_email(value: str):
    if not value:
        raise ValidationError
    
    if not ("@" in value and "." in value):
        raise ValidationError
    
    user_part, _, domain_part = value.partition("@")
    
    if not (re.match(EMAIL_USER_PART, user_part)
            and re.match(EMAIL_DOMAIN_PART, domain_part)):
        raise ValidationError
