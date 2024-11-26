from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class AppointmentForm(FlaskForm):
    pet_owner = StringField('飼い主様のお名前', validators=[DataRequired(), Length(max=100)])
    pet_name = StringField('ペットのお名前', validators=[DataRequired(), Length(max=100)])
    pet_type = SelectField('ペットの種類', 
                          choices=[('犬', '犬'), ('猫', '猫'), ('鳥', '鳥'), ('その他', 'その他')],
                          validators=[DataRequired()])
    phone = StringField('電話番号', validators=[DataRequired(), Length(max=20)])
    email = EmailField('メールアドレス', validators=[DataRequired(), Email()])
    appointment_date = DateField('予約希望日', validators=[DataRequired()])
    appointment_time = SelectField('予約希望時間',
                                 choices=[('9:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'),
                                        ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'),
                                        ('17:00', '17:00')],
                                 validators=[DataRequired()])
    reason = TextAreaField('ご来院の理由', validators=[DataRequired()])

class ContactForm(FlaskForm):
    name = StringField('お名前', validators=[DataRequired(), Length(max=100)])
    email = EmailField('メールアドレス', validators=[DataRequired(), Email()])
    message = TextAreaField('お問い合わせ内容', validators=[DataRequired()])

class AdminLoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])

class AppointmentStatusForm(FlaskForm):
    status = SelectField('ステータス',
                        choices=[('pending', '未対応'), ('confirmed', '確認済み'),
                                ('completed', '完了'), ('cancelled', 'キャンセル')],
                        validators=[DataRequired()])

class ContactStatusForm(FlaskForm):
    status = SelectField('ステータス',
                        choices=[('unread', '未読'), ('read', '既読'), ('replied', '返信済み')],
                        validators=[DataRequired()])
