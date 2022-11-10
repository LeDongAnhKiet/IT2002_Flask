from flask import render_template, request, redirect
from app import app, dao, admin, login
from flask_login import login_user
import cloudinary.uploader


@app.route('/')
def index():
    products = dao.load_products(category_id=request.args.get('category_id'),
                                 kw=request.args.get('keyword'))
    return render_template('index.html', products=products)


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def user_login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = dao.auth_user(username=username,password=password)
        if user:
            login_user(user=user)
            return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                print(res)
                avatar = res['secure_url']
            try:
                dao.register(name=request.form['name'],
                         password=password,
                         username=request.form['username'], avatar=avatar)
                return redirect('/login')
            except:
                err_msg = 'Lỗi! Hãy quay lại sau.'
        else: err_msg = 'Mật khẩu KHÔNG khớp!'
    return render_template('register.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories
    }

if __name__ == '__main__':
    app.run(debug=True)
