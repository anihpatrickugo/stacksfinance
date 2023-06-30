
import datetime
from django import forms



def age_validator(dob):
    age = datetime.date.today() - dob
    final_age = int(age.days / 356.25)

    if final_age < 16:
        raise forms.ValidationError('Must be above 16 years old')