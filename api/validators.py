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

PASSWORD_MUST_HAVE = (
    re.compile(r"[A-Z]"),
    re.compile(r"[a-z]"),
    re.compile(r"[0-9]"),
    # Symbols taken from OWASP list of characters found in passwords, minus whitespace
    #  and brackets.
    re.compile(r"!#\$%&\*+,-\./:<;=\?>@\^_\|~"),
)
PASSWORD_MUST_NOT_HAVE = (
    re.compile(r"\s"),
    # Must not contain anything that isn't in the allowed/required characters.
    re.compile(
        f"[^"
        f"{''.join(condition.pattern.strip('[]') for condition in PASSWORD_MUST_HAVE)}"
        f"]"
    ),
)


def validate_email(value: str):
    """Verify that the input is a valid (not necessarily registered) email address."""
    if not value:
        raise ValidationError

    if not ("@" in value and "." in value):
        raise ValidationError

    user_part, _, domain_part = value.partition("@")

    if not (
        re.match(EMAIL_USER_PART, user_part)
        and re.match(EMAIL_DOMAIN_PART, domain_part)
    ):
        raise ValidationError


def validate_password(value: str):
    """Verify that the input is a reasonably secure password."""
    if not value or len(value) < 12:
        raise ValidationError("Password is too short.")

    if any(re.search(condition, value) for condition in PASSWORD_MUST_HAVE):
        raise ValidationError("Password does not have all necessary minimum symbols.")

    if any(re.search(condition, value) for condition in PASSWORD_MUST_NOT_HAVE):
        raise ValidationError("Password includes disallowed characters.")
