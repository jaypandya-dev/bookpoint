import re

def validate(password: str) -> bool:
  if len(password) < 8:
    return False

  capital_pattern = "[A-Z]+"
  if re.search(capital_pattern, password) is None:
    return False
  
  small_pattern = "[a-z]+"
  if re.search(small_pattern, password) is None:
    return False
  
  number_pattern = "[0-9]+"
  if re.search(number_pattern, password) is None:
    return False
  
  special_char = "\\W+"
  if re.search(special_char, password) is None:
    return False

  return True