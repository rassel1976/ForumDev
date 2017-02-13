from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from Forum.models import Comment, Post, CustomUser, Avatar, Document, FMessage, OMessage
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.text import capfirst

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_text','post_name']

class UploadAvatarForm(ModelForm):
    class Meta:
        model = Avatar
        fields = ['avatar']


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as before, for verification."))

    class Meta:
        model = CustomUser
        fields = ("username","email", "avatar")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ( 'document', )

class SearchForm(forms.Form):
    search = forms.CharField(max_length=255)

class FMessageForm(forms.ModelForm):
    class Meta:
        model = FMessage
        fields = ['message',]

class OMessageForm(forms.ModelForm):
    class Meta:
        model = OMessage
        fields = ['message']