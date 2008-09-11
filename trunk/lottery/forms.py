from django import forms

class FilterDraw(forms.Form):
    from_date = forms.DateField()
    till_date = forms.DateField()
    is_drawen = forms.BooleanField(required=False)
    logical_and = forms.BooleanField(required=False)
    numbers = forms.CharField(max_length=200)

class LuckyForm(forms.Form):
    lucky = forms.CharField()
    check = forms.CharField()