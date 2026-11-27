from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


INITIAL_PATTERN = r"\A[A-Z][.]\Z"
A_MODEL_PATTERN = r"\AA-[1-9][0-9]*\Z"
S_MODEL_PATTERN = r"\AS-[1-9][0-9]*\Z"

# Passenger middle initials and crew first initials use one uppercase letter and a period, like K.
initial_validator = RegexValidator(INITIAL_PATTERN, "Enter an uppercase initial followed by a period.")

# A-series model codes use A- followed by a positive integer with no leading zeros, like A-12.
a_model_validator = RegexValidator(A_MODEL_PATTERN, "Enter a model code like A-12.")

# S-series model codes use S- followed by a positive integer with no leading zeros, like S-3.
s_model_validator = RegexValidator(S_MODEL_PATTERN, "Enter a model code like S-3.")


# Birth, purchase, and maintenance dates must be today or earlier.
def validate_not_future(value):
    if value > timezone.localdate():
        raise ValidationError("Enter today’s date or an earlier date.")
