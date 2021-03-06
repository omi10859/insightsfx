from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from .models import User
from django.core.validators import validate_email
from .utils import UserExistsByEmail

class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput,
        label="Email"
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.label_class = "font-weight-bold"
        self.helper.form_error_title = "Oops"
        self.helper.add_input(
            Submit('login', 'Login', css_class="btn-block")
        )


class UserSignupForm(ModelForm):

    first_name = forms.CharField(
        required=True
    )
    last_name = forms.CharField(
        required=True
    )
    gender = forms.ChoiceField(
        choices=User.gender_choices,
        widget=forms.widgets.RadioSelect
    )
    mobile = forms.CharField(
        required = True,
        label = 'Mobile Number'
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label='Password'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'mobile',
        ]

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "container"
        self.helper.label_class = "font-weight-bold"

        self.helper.layout = Layout(
            Div(
                Field('first_name', wrapper_class="col-12 col-md-6"),
                Field('last_name', wrapper_class="col-12 col-md-6"),
                css_class="row"
            ),
            'mobile',
            'email',
            'password1',
            InlineRadios('gender'),
            HTML(
                '<div class="my-3">By Signing up, you automatically agree to our <a href="#">Terms and Conditions</a>.</div>',
            )
        )
        self.helper.add_input(
            Submit('register', 'Create New Account', css_class="btn-block")
        )

    def save(self, commit=True):
        m = super(UserSignupForm, self).save(commit=False)

        m.set_password(self.cleaned_data['password1'])

        if commit:
            m.save()
        return m

class EmailCollectionForm(forms.Form):

    email = forms.EmailField(label="Enter your email", required=True)

    def __init__(self, *args, **kwargs):
        super(EmailCollectionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.label_class = "font-weight-bold"
        self.helper.form_error_title = "Oops"
        self.helper.add_input(
            Submit('submit', 'Submit', css_class="btn-block")
        )
    
    def clean_email(self):

        validate_email(self.cleaned_data['email'])

        if not UserExistsByEmail(self.cleaned_data['email']):
            raise ValidationError("An account with the given email doesn't exist")

        return self.cleaned_data['email']