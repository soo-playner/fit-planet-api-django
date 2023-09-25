from django.core.exceptions import ValidationError
import re

class CustomValidator:
  def password_validate(password):
    if (
      len(password) < 8 or
      not re.search(r"[a-zA-Z]", password) or
      not re.search(r"\d", password) or
      not re.search(r"[~'!@#$%^&*()]", password)
    ):
      return 400
    return 200