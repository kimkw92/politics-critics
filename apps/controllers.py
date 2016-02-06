# -*- encoding:utf-8 -*-

from flask import Flask, redirect, url_for, render_template,request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from apps import app, db
from models import Article, Comment, User
from form import JoinForm, LoginForm
from sqlalchemy import desc
import pusher

# 메인페이지 입니다
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/new', methods = ['GET', 'POST'])
def new_article():
	if not 'session_user_email' in session:
		flash(u"로그인 해주세요.")
		return redirect(url_for('login'))

	if request.method == 'GET':
		return render_template("write.html", active_tab = "new")

	user = User.query.get(session['session_user_email'])

	this = Article(
		title = request.form['title'],
		content = request.form['content'],
		author = user.name,
		user = user)

	db.session.add(this)
	db.session.commit()

	flash(u"잘 저장되었습니다.")

	return redirect(url_for("index"))

@app.route('/detail/<int:id>')
def detail(id):
	this = Article.query.get(id)
	this_comment = Comment.query.filter_by(article_id=this.id)
	# this_comment = Comment.query.get(id)
	return render_template("detail.html", this = this, this_comment = this_comment)

@app.route('/delete/<int:id>')
def remove(id):
	this = Article.query.get(id)
	author_email = this.user.email

	if not 'session_user_email' in session:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=id))

	elif session['session_user_level'] == 10 or session['session_user_email'] == author_email:
		db.session.delete(this)
		db.session.commit()
		flash(u"삭제되었습니다.")
		return redirect(url_for("index"))
	
	else :
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=id))


	# return redirect(url_for("index"))
@app.route('/modify/<int:id>',methods = ['GET', 'POST'])
def modify(id):
	this = Article.query.get(id)
	author_email = this.user.email

	# if request.method == 'GET':	
	# 	return render_template("modify.html", this = this)

	if not 'session_user_email' in session:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=id))

	elif session['session_user_email'] != author_email:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=id))

	elif request.method=='POST':

		this.title = request.form['title']
		this.content = request.form['content']
		this.category = request.form['category']
	
		db.session.commit()

		flash(u"수정되었습니다..")

		return redirect(url_for("index"))

	else : 
	# session['session_user_level'] == 10 or session['session_user_email'] == author_email:
		return render_template("modify.html", this=this)

	# if request.method=='POST':

	# 	this.title = request.form['title']
	# 	this.content = request.form['content']
	# 	this.category = request.form['category']
	
	# 	db.session.commit()

	# 	flash(u"수정되었습니다..")

	# 	return redirect(url_for("index"))
@app.route('/like/<int:id>', methods = ['GET', 'POST'])
def like(id):

	this = Article.query.get(id)
	this.like = this.like + 1
	
	db.session.commit()

	return redirect(url_for("detail", id=id))

@app.route('/hate/<int:id>', methods = ['GET', 'POST'])
def hate(id):

	this = Article.query.get(id)
	this.hate = this.hate + 1
	
	db.session.commit()

	return redirect(url_for("detail", id=id))

@app.route('/comment/new/<int:id>', methods = ['GET', 'POST'])
def comment_create(id):
	this = Article.query.get(id)
	author_email = this.user.email
	
	if not 'session_user_email' in session:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=id))

	elif request.method=='POST':
		user = User.query.get(session['session_user_email'])
		this_comment = Comment(
		author = user.name,
		# password = request.form['password'],
		content = request.form['content'],
		article_id = id,
		user = user
		)

		db.session.add(this_comment)
		db.session.commit()
		flash(u"수정되었습니다..")
		return redirect(url_for("detail", id=id))	

	else:
		return render_template("comment_create.html", this=this)	
	

@app.route('/comment/delete/<int:id>')
def comment_delete(id):

	this_comment = Comment.query.get(id)
	author_email = this_comment.user.email

	if not 'session_user_email' in session:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=this_comment.article_id))

	elif session['session_user_level'] == 10 or session['session_user_email'] == author_email:
		db.session.delete(this_comment)
		db.session.commit()
		flash(u"삭제되었습니다.")
		return redirect(url_for("detail", id=this_comment.article_id))
	
	else :
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=this_comment.article_id))


@app.route('/comment/modify/<int:id>',methods = ['GET', 'POST'])
def comment_modify(id):

	this_comment = Comment.query.get(id)
	author_email = this_comment.user.email

	if not 'session_user_email' in session:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=this_comment.article_id))

	elif session['session_user_email'] != author_email:
		flash(u"권한이 없습니다.")
		return redirect(url_for("detail", id=this_comment.article_id))

	elif request.method=='POST':

		this_comment.content = request.form['content']
		db.session.commit()
		flash(u"수정되었습니다..")
		return redirect(url_for("detail", id=this_comment.article_id))	
	else:
		return render_template("comment_modify.html", this_comment=this_comment)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	form = JoinForm()

	if request.method == 'GET':
		return render_template("signup.html", form =form)

	if not form.validate_on_submit():
		return render_template("signup.html", form=form)

	user = User(email = form.email.data, password = generate_password_hash(form.password.data), name = form.name.data)

	db.session.add(user)
	db.session.commit()

	flash(u"회원가입이 되었습니다.")

	session['session_user_email'] = user.email
	session['session_user_name'] = user.name
	session['session_user_level'] = user.level
	
	return redirect(url_for('index'))


@app.route('/signin', methods = ['GET', 'POST'])
def login():

	if request.method == "GET":
		return render_template('login.html')

	user_email = request.form['email']
	user_password = request.form['password']

	user = User.query.get(user_email)

	if user is None:
		flash(u"없는 아이디입니다.")
		return redirect(url_for("login"))
	if not check_password_hash(user.password, user_password):
		flash(u"비밀번호가 틀렸습니다.")
		return redirect(url_for("login"))

	session['session_user_email'] = user.email
	session['session_user_name'] = user.name
	session['session_user_level'] = user.level

	return redirect(url_for('index'))

	# if request.method == "GET":
	# 	return render_template("login.html")

@app.route('/signout')
def logout():
	if "session_user_email" in session:
		session.clear()
		flash(u"로그아웃 되었습니다.")
	else:
		flash(u"로그인 되어있지 않습니다.")
	return redirect(url_for('index'))

@app.route('/rows')
def rows():

	rows_from_server = Article.query.count()
	return jsonify(rows=rows_from_server)

@app.route('/more')
def more():

	data_from_ajax = request.args['number']
	one_article = Article.query.get(data_from_ajax)
	
	id_sql = one_article.id
	title_sql = one_article.title
	content_sql = one_article.content
	author_sql = one_article.author

	return jsonify(id = id_sql, title = title_sql, content = content_sql, author = author_sql)

@app.route('/ajax_ex', methods = ['GET', 'POST'])
def ajax_ex():

	if request.method == "POST":

		value = request.form['from_html']

		p = pusher.Pusher(app_id='86964', key='de42785da4ca0d2657a1', secret='0a4dd538596072c7c732')

		p['sasung_channel'].trigger('my_event', {'from_server': value})	
		
		return jsonify()


	return render_template("chatting.html")



