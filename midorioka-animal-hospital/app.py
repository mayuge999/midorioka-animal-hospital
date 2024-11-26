import os
from datetime import datetime
import pytz
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

JST = pytz.timezone('Asia/Tokyo')
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin_login'  # type: ignore

from models import Admin, Appointment, Contact
from forms import AppointmentForm, ContactForm, AdminLoginForm, AppointmentStatusForm, ContactStatusForm

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

def nl2br(value):
    if not value:
        return ""
    return value.replace('\n', '<br>')

app.jinja_env.filters['nl2br'] = nl2br


@app.route('/price-list')
def price_list():
    return render_template('price_list.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    form = AppointmentForm()
    if form.validate_on_submit():
        try:
            appointment = Appointment()
            appointment.pet_owner = form.pet_owner.data
            appointment.pet_name = form.pet_name.data
            appointment.pet_type = form.pet_type.data
            appointment.phone = form.phone.data
            appointment.email = form.email.data
            appointment.appointment_date = form.appointment_date.data
            appointment.appointment_time = datetime.strptime(form.appointment_time.data, '%H:%M').time()
            appointment.reason = form.reason.data
            appointment.status = 'pending'
            db.session.add(appointment)
            db.session.commit()
            flash('ご予約ありがとうございます。確認メールをお送りいたします。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('予約の登録中にエラーが発生しました。お手数ですが、しばらく経ってからもう一度お試しください。', 'danger')
            app.logger.error(f'予約登録エラー: {str(e)}')
    return render_template('reservation.html', form=form)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        try:
            admin = Admin.query.filter_by(username=form.username.data).first()
            if admin and admin.password_hash:
                if check_password_hash(admin.password_hash, form.password.data):
                    login_user(admin)
                    flash('管理者としてログインしました。', 'success')
                    return redirect(url_for('admin_dashboard'))
            flash('ユーザー名またはパスワードが正しくありません。', 'danger')
        except Exception as e:
            app.logger.error(f'ログインエラー: {str(e)}')
            flash('ログイン処理中にエラーが発生しました。お手数ですが、しばらく経ってからもう一度お試しください。', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/dashboard.html', appointments=appointments, contacts=contacts)

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/admin/appointments/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_appointment_detail(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentStatusForm(obj=appointment)
    if form.validate_on_submit():
        appointment.status = form.status.data
        db.session.commit()
        flash('予約状態を更新しました。', 'success')
        return redirect(url_for('admin_appointments'))
    return render_template('admin/appointment_detail.html', appointment=appointment, form=form)

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # パフォーマンス最適化：必要なカラムのみを取得
        query = Contact.query.options(
            db.load_only(Contact.id, Contact.name, Contact.email, 
                        Contact.message, Contact.status, Contact.created_at)
        ).order_by(Contact.created_at.desc())
        
        # ページネーション処理
        contacts = query.paginate(page=page, per_page=per_page, error_out=False)
        
        if not contacts.items and page > 1:
            return redirect(url_for('admin_contacts', page=1))
            
        return render_template('admin/contacts.html',
                             contacts=contacts.items,
                             page=page,
                             total_pages=contacts.pages,
                             max=max,  # builtins.maxをテンプレートに追加
                             min=min)  # builtins.minをテンプレートに追加
    except Exception as e:
        app.logger.error(f'お問い合わせ一覧取得エラー: {str(e)}')
        flash('お問い合わせ情報の取得中にエラーが発生しました。', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/contacts/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_contact_detail(id):
    try:
        # 必要なカラムのみを取得して最適化
        contact = Contact.query.options(
            db.load_only(Contact.id, Contact.name, Contact.email, 
                        Contact.message, Contact.status, Contact.created_at)
        ).get_or_404(id)
        
        form = ContactStatusForm(obj=contact)
        
        if form.validate_on_submit():
            try:
                contact.status = form.status.data
                db.session.commit()
                flash('お問い合わせ状態を更新しました。', 'success')
                return redirect(url_for('admin_contacts'))
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'ステータス更新エラー: {str(e)}')
                flash('ステータスの更新中にエラーが発生しました。', 'danger')
                return redirect(url_for('admin_contacts'))
        return render_template('admin/contact_detail.html', contact=contact, form=form)
    except Exception as e:
        app.logger.error(f'お問い合わせ詳細取得エラー: {str(e)}')
        flash('お問い合わせ情報の取得中にエラーが発生しました。', 'danger')
        return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/<int:id>/update-status', methods=['POST'])
@login_required
def update_contact_status(id):
    try:
        data = request.get_json()
        contact = Contact.query.get_or_404(id)
        contact.status = data.get('status')
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f'ステータス更新APIエラー: {str(e)}')
        return jsonify({'error': 'ステータス更新に失敗しました'}), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact()
        contact.name = form.name.data
        contact.email = form.email.data
        contact.message = form.message.data
        db.session.add(contact)
        db.session.commit()
        flash('お問い合わせありがとうございます。担当者より返信させていただきます。', 'success')
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)

# Initialize database and configure login manager
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
