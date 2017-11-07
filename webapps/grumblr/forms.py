from django import forms
from models import *
class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'username',
        max_length = 32
    )
    firstname = forms.CharField(
        required=True,
        label='firstname',
        max_length=32
    )
    lastname = forms.CharField(
        required=True,
        label='lastname',
        max_length=32
    )
    email = forms.CharField(
        required = True,
        label = 'email',
        max_length = 32,
    )

    password = forms.CharField(
        required = True,
        label = 'password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    passwordrepeat = forms.CharField(
        required = True,
        label = 'passwordrepeat',
        max_length = 32,
        widget = forms.PasswordInput()
    )

    def clean_passwordrepeat(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data.get("passwordrepeat", "")
        if password1 and password2:  # If both passwords has value
            if password1 != password2:
                raise forms.ValidationError((u"Passwords didn't match."))
        else:
            raise forms.ValidationError((u"Passwords can't be blank."))
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {'picture': forms.FileInput()}

class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        required = True,
        label = 'password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    passwordrepeat = forms.CharField(
        required = True,
        label = 'passwordrepeat',
        max_length = 32,
        widget = forms.PasswordInput()
    )

    def clean_passwordrepeat(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data.get("passwordrepeat", "")
        if password1 and password2:  # If both passwords has value
            if password1 != password2:
                #print "doesn't match"
                raise forms.ValidationError((u"Passwords didn't match."))
        else:
            raise forms.ValidationError((u"Passwords can't be blank."))
        return password2


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)






