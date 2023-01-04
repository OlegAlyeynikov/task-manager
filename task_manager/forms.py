from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core import exceptions

from django.db.models import enums
from django.forms import BaseForm

from task_manager.models import Worker, Task


class WorkerLoginForm(forms.Form, BaseForm):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(
            attrs={"class": "form-control  mb-3", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "Password"}
        ),
    )


class WorkerRegisterForm(forms.ModelForm, BaseForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)

    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    time_zone = forms.ChoiceField(label="Time zone", choices=enums.TIME_ZONE_CHOICES)

    class Meta:
        model = Worker
        fields = ["username", "email", "position", "time_zone"]

    def clean(self):
        """
        Validate attributes, including password constraints, before persisting the user to the database.
        """
        super(WorkerRegisterForm, self).clean()

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("You must enter matching passwords.")

        try:
            password_validation.validate_password(
                password=password1, user=get_user_model()
            )
        except exceptions.ValidationError as e:
            raise forms.ValidationError(list(e.messages))

    def save(self, commit=True):
        """
        Save the provided password in hashed format.

        :param commit: If True, changes to the instance will be saved to the database.
        """
        user = super(WorkerRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()

        return user


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task name.."}),
    )
