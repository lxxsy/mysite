from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class SignInForm(forms.Form):
    username = forms.CharField(
        label='用户名', 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'}
        )
    )
    password = forms.CharField(
        label='密码', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        )
    )
    # 当执行form.is_valid()时，例如【if sign_in_form.is_valid():】,会对每个field进行检查，并立即产生cleaned_data的数据，
    # 如果有clean或clean_开头的方法，则开始执行此函数(此时cleaned_data的数据已经可以用了)
    # 因为字段数据已经被指定字段的默认校验逻辑执行完毕了，说明校验通过，cleaned_data就会有数据，同样，我们不必担心数据是否为空，因为它已经被校验过了
    # 注意：如果校验不通过不会执行clean或clean_开头的方法
    def clean(self):
        # 数据已经合法，进行提取
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # 验证此用户
        user = authenticate(username=username, password=password)
        # 不存在，抛出异常
        if user is None:
            print('xxx')
            raise forms.ValidationError('用户名或密码不正确')
        # 反之添加user用户并返回
        else:
            self.cleaned_data['user'] = user
        print('xxxxxx')
        return self.cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(
        label='用户名', 
        max_length='30',
        min_length='3',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'}
        )
    )
    email = forms.CharField(
        label='邮箱', 
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )
    password = forms.CharField(
        label='密码', 
        min_length='6', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        )
    )
    password_again = forms.CharField(
        label='再次输入密码', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}
        )
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')

        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data


class NicknameChangeForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称', 
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空')
        return self.cleaned_data

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请发送验证码到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        # 判断此用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('您已经绑定邮箱')
        # 判断邮箱
        email = self.cleaned_data.get('email', '').strip()
        if email == '':
            raise forms.ValidationError('邮箱不能为空')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        print(code)
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data


    