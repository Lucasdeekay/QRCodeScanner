from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError("Field cannot be empty")


class ForgotPasswordForm(forms.Form):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your staff id/matric no',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        user_id = cleaned_data.get('user_id')
        email = cleaned_data.get('email')
        if not user_id or not email:
            raise forms.ValidationError("Field cannot be empty")


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your matric no / staff id',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    department = forms.CharField(
        help_text="Select programme if staff",
        max_length=30,
        widget=forms.Select(
            choices=[
                (' Science', 'Select Department'),
                ('Computer Science', 'Computer Science'),
                ('Biological Science', 'Biological Science'),
                ('Chemical Science', 'Chemical Science'),
                ('Business Administration', 'Business Administration'),
                ('Mass Communication', 'Mass Communication'),
                ('Criminology', 'Criminology'),
                ('Accounting', 'Accounting'),
            ],
            attrs={
                'class': 'form-control',
            }
        )
    )
    programme = forms.CharField(
        max_length=30,
        help_text="Select programme if student",
        widget=forms.Select(
            choices=[
                ('', 'Select Programme'),
                ('Computer Science', 'Computer Science'),
                ('Software Engineering', 'Software Engineering'),
                ('Cyber Security', 'Cyber Security'),
                ('Biochemistry', 'Biochemistry'),
                ('Industrial Chemistry', 'Industrial Chemistry'),
                ('Business Administration', 'Business Administration'),
                ('Mass Communication', 'Mass Communication'),
                ('Criminology', 'Criminology'),
                ('Microbiology', 'Microbiology'),
                ('Economics', 'Economics'),
                ('Accounting', 'Accounting'),
            ],
            attrs={
                'placeholder': 'Enter your programme',
                'class': 'form-control',
            }
        )
    )
    level = forms.CharField(
        max_length=30,
        help_text="Select level if student",
        widget=forms.Select(
            choices=[
                ('', 'Select Level'),
                ('100', '100'),
                ('200', '200'),
                ('300', '300'),
                ('400', '400'),
            ],
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        full_name = cleaned_data.get('full_name')
        email = cleaned_data.get('email')
        user_id = cleaned_data.get('user_id')
        level = cleaned_data.get('level')
        programme = cleaned_data.get('programme')
        department = cleaned_data.get('last_name')
        if not full_name or not email or not user_id:
            raise forms.ValidationError("Field cannot be empty")


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        help_text="Minimum of 8 characters",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': '',
                'class': 'form-control form-control-sm rounded bright',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'required': '',
                'class': 'form-control form-control-sm rounded bright',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")


class CourseForm(forms.Form):
    course_title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Course Title',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    course_code = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Course Code',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    course_unit = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Course Unit',
                'required': '',
                'class': 'form-control',
            }
        )
    )
    semester = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('', 'Select Semester'),
                ('1st', '1st'),
                ('2nd', '2nd'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )
    department = forms.CharField(
        max_length=30,
        widget=forms.Select(
            choices=[
                ('Computer Science', 'Computer Science'),
                ('Biological Science', 'Biological Science'),
                ('Chemical Science', 'Chemical Science'),
                ('Business Administration', 'Business Administration'),
                ('Mass Communication', 'Mass Communication'),
                ('Criminology', 'Criminology'),
                ('Accounting', 'Accounting'),
            ],
            attrs={
                'required': '',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        course_title = cleaned_data.get('course_title')
        course_code = cleaned_data.get('course_code')
        course_unit = cleaned_data.get('course_unit')
        semester = cleaned_data.get('semester')
        department = cleaned_data.get('last_name')
        if not course_title or not course_code or not course_unit or not semester or not department:
            raise forms.ValidationError("Field cannot be empty")
