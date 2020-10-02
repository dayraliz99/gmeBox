from django import forms
from django.contrib.auth import forms as auth_forms
from people.models import Usuario
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import admin as auth_admin

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = Usuario
        fields = ('correo_electronico',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label=_("Password"),
                                                    help_text=_("Raw passwords are not stored, so there is no way to see "
                                                                "this user's password, but you can change the password "
                                                                "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyAdminPasswordChangeForm(auth_admin.AdminPasswordChangeForm):

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password = self.cleaned_data["password"]
        self.user.myuser.set_password(password)
        if commit:
            self.user.myuser.save()
        return self.user.myuser
