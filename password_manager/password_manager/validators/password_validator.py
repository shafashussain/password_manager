from django.core.exceptions import ValidationError


def password_validator(password):
     
    SpecialSym =['$', '@', '#', '%']
     
    if len(password) < 6:
        raise ValidationError("length should be at least 6")
         
    if len(password) > 20:
        raise ValidationError("length should be not be greater than 20")
         
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password should have at least one numeral")
         
    if not any(char.isupper() for char in password):
        raise ValidationError("Password should have at least one uppercase letter")
         
    if not any(char.islower() for char in password):
        raise ValidationError("Password should have at least one lowercase letter")
         
    if not any(char in SpecialSym for char in password):
        raise ValidationError("Password should have at least one of the symbols $@#")
    return password