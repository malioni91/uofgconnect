from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class UserForm(forms.ModelForm):
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password', 'confirm_password')

    def clean_name(self):
	full_name = self.cleaned_data.get('name').split()
        if len(full_name) == 1:
            self.instance.first_name = full_name[0]
        elif len(full_name) >= 3:
            self.instance.first_name = full_name[0]
            self.instance.last_name = " ".join(full_name[1:])
        else:
            self.instance.first_name = full_name[0]
            self.instance.last_name = full_name[1]
        return self.cleaned_data

    def clean(self):
	super(UserForm, self).clean()
	password = self.cleaned_data.get('password')
	confirm_password = self.cleaned_data.get('confirm_password')
        if not password:
            raise forms.ValidationError(mark_safe("Empty password. Try again."))
	if password and password != confirm_password:
	    raise forms.ValidationError(mark_safe("Passwords do not match. Try again."))
	return self.cleaned_data
