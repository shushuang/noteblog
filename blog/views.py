from pyramid.i18n import TranslationStringFactory
from pyramid.response import Response
from pyramid.httpexceptions import (
	HTTPFound,
	HTTPNotFound
	)
from pyramid.view import view_config
from pyramid.session import check_csrf_token
from sqlalchemy.exc import DBAPIError
from .models import (
	Blog,
	BlogClass,
	User,
	)
from blog import DBSession
import logging
import cgi
import hashlib
from datetime import datetime
from jinja2 import Template
# _ = TranslationStringFactory('blog')
log = logging.getLogger(__name__)


@view_config(route_name='view_blogs', renderer='templates/view_blogs.html')
def view_blogs(request):
	user_id = request.session['user_id']
	dbsession = DBSession()
	blogs = dbsession.query(Blog).filter_by(user_id=user_id).all()
	return {'blogs':blogs}


@view_config(route_name='add_blog', renderer='templates/add_blog.html')
def add_blog(request):
	log.info('start add blog')
	if 'form.submitted' in request.params:
		check_csrf_token(request)
		user_id = request.session['user_id']
		default_class_id = DBSession().query(BlogClass).filter_by(id = request.session['user_id'],
							name = 'all').one()
		blog = Blog(title = request.params['title'], 
			content = request.params['content'],
			created_time = datetime.today(),
			)
		# created_time = cgi.escape(request.params['content']))
		DBSession.add(blog)
# 		insert blog blog_class realtionships
		blogclass_names = request.params['class_names'].split(';')
		for blogclass_name in blogclass_names:
			blogclass = DBSession().query(BlogClass).filter_by(
						name = blog_class.name).one()
			blog = DBSession().query(Blog).filter_by(
						title = blog.title).one()
			blog_blogclass = Blog_BlogClass(blog_id= blog.id, blogclass_id = blogclass.id)
			DBSession.add(blog_blogclass)
		log.info('add_blog submitted')
		return HTTPFound(request.route_url('view_blog'
			))
	log.info('add_blog view')
	return dict()
#use ajax to add a blogclass
@view_config(route_name = 'add_blogclass', renderer = 'json')
def add_blogclass(request):
	blogclass_name = request.params['blogclass_name']
	blogclass= BlogClass(name = request.params['blogclass_name'])
	DBSession().add(blogclass)
	return dict(result = 'ok')
#use ajax to load blog classes 
@view_config(route_name = 'get_blogclasses', renderer = 'json')
def get_blogclasses(request):
	blogclasses = DBSession().query(BlogClass).filter_by(
		user_id = request.session['user_id']).all()
	template = Template('''
			{% for blogclass in blogclasses %}
		        <li>{{blogclass.name}}</li>
		    {% endfor %}		
	''');
	htmlval = template.render(blogclasses = blogclasses)
	return dict(htmlval = htmlval)
#when in view page link edit
#when in edit page submit
@view_config(route_name='edit_blog', renderer='templates/edit_blog.html')
def edit_blog(request):
	if 'form.submitted' in request.params:
		check_csrf_token(request)
		blog_id = request.matchdict['blog_id']
		DBSession().query(Blog).filter_by(id=blog_id).update({
				'title': request.params['title'],
				'content': request.params['content'],
				'last_modified_time': datetime.today(),
				})
		log.info('submit in edit page')
		return HTTPFound(request.route_url('view_blog'))
	blog_id = request.matchdict['blog_id']
	saved_url = request.route_url('edit_blog', blog_id = blog_id)
	theblog = DBSession().query(Blog).filter_by(id=blog_id).one()
	log.info('link in view page')
	return dict(blog = theblog, actionurl=saved_url)

@view_config(route_name='signup', renderer='templates/signup.html')
def signup(request):
	if 'form.submitted' in request.params:
		name = request.params['name']
		email = request.params['email']
		pwd = request.params['pwd']
		anopwd = request.params['anopwd']
		if pwd!=anopwd:
			return HTTPFound(request.route_url('signup'))
		m = hashlib.sha1(pwd)
		hashedpwd = m.hexdigest()
		user = User(name=name, pwd=hashedpwd, email=email)
		DBSession().add(user)
		user = DBSession().query(User).filter_by(email=email).one()
		request.session['user_id'] = user.id
		#add a blog class named """all"""
		default_blog_class = BlogClass(user_id = user.id, name="all")
		DBSession().add(default_blog_class)
		return HTTPFound(request.route_url('view_blogs'))
	log.info('enter signup page')
	return dict()

@view_config(route_name='admin', renderer='templates/users.html')
def getusers(request):
	users = DBSession().query(User).all()
	return dict(users=users)

@view_config(route_name='validname',renderer='json')
def check_user_unique(request):
	users = DBSession().query(User).all()
	for user in users:
		if user.name==request.params['name']:
			return {'valid':'no'}
		else:
			return {'valid':'yes'}
@view_config(route_name='signin',renderer='templates/signin.html')
def sign_in(request):
	if 'form.submitted' in request.params:
		email=request.params['email']
		pwd = request.params['pwd']
		m = hashlib.sha1(pwd)
		hashedpwd = m.hexdigest()
		logined_user = DBSession().query(User).filter_by(email=email, pwd=hashedpwd).first()
		if logined_user == None:
			return dict(wrong='true')
		request.session['user_id']=logined_user.id
		return HTTPFound(request.route_url('view_blogs'))
	return dict()