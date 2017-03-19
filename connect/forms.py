from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from connect.models import Course, UserProfile
from django.contrib.auth import authenticate



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
        email = self.cleaned_data.get('email')
        if not password:
            raise forms.ValidationError(mark_safe("Empty password. Try again."))
        if password and password != confirm_password:
            raise forms.ValidationError(mark_safe("Passwords do not match. Try again."))
        if "@student.gla.ac.uk" not in email and "@gla.ac.uk" not in email:
            raise forms.ValidationError("You email is not a valid UofG email address.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used.")
        return self.cleaned_data

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Authentication failed. Please try again.")
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ('course',)



class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class EditForm(forms.ModelForm):
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password', 'new_password', 'confirm_password')

    def clean_name(self):
        print 'invalid12'
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
        super(EditForm, self).clean()
        password = self.cleaned_data.get('password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        email = self.cleaned_data.get('email')
        if not password:
            raise forms.ValidationError(mark_safe("Empty password. Try again."))
        if new_password != confirm_password:
                raise forms.ValidationError(mark_safe("Passwords do not match. Try again."))
        if "@student.gla.ac.uk" not in email and "@gla.ac.uk" not in email:
            raise forms.ValidationError("You email is not a valid UofG email address.")
        return self.cleaned_data
