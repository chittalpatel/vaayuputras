from django import forms

# Djnago form for taking CSV file and capacity from user which is used for training model
class UploadFileForm(forms.Form):
    capacity = forms.FloatField(required=True,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Capacity of Turbine/Farm','id':'cap'}))
    file = forms.FileField(required=True,widget=forms.FileInput(attrs={'accept':'.csv','id':'fileUpload','onchange':"ValidateSize(this)"}))