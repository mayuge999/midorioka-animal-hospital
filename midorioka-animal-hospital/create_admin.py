import os
from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def create_initial_admin():
    default_username = 'admin'
    default_password = 'admin123'  # This will be used only if environment variables are not set
    
    admin_username = os.environ.get('ADMIN_USERNAME', default_username)
    admin_password = os.environ.get('ADMIN_PASSWORD', default_password)

    with app.app_context():
        # Check if admin account exists
        existing_admin = Admin.query.filter_by(username=admin_username).first()
        if existing_admin is None:
            # Create new Admin instance
            new_admin = Admin()
            new_admin.username = admin_username
            new_admin.password_hash = generate_password_hash(admin_password)
            
            # Add to database
            db.session.add(new_admin)
            db.session.commit()
            
            print('管理者アカウントを作成しました。')
            print(f'ユーザー名: {admin_username}')
            print('パスワードは環境変数で設定された値です。')
        else:
            print('管理者アカウントは既に存在します。')

if __name__ == '__main__':
    create_initial_admin()
