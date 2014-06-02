from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from zope.sqlalchemy import ZopeTransactionExtension

# from .models import (
#     DBSession,
#     Base,
# )
DBSession = scoped_session(sessionmaker(extension = ZopeTransactionExtension()))
Base = declarative_base()
def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)
    Base.metadata.bind = engine
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'blog')
    config = Configurator(settings=settings)
    #session set
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config.set_session_factory(my_session_factory)
    #session set end
    config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_static_view('static', 'static', cache_max_age = 3600)
    # config.add_view('blog.views.my_view',
    #                 context='blog.models.MyModel', 
    #                 renderer="templates/mytemplate.jinja2")
    config.add_route('view_blogs', '/view_blogs')
    config.add_route('edit_blog','/edit_blog/{blog_id}')
    config.add_route('add_blog', '/add_blog')
    config.add_route('signup','/signup')
    config.add_route('admin','/admin')
    config.add_route('validname', '/validname')
    config.add_route('signin','/signin')
    config.add_route('add_blogclass','/add_blogclass')
    config.add_route('get_blogclasses', '/get_blogclasses')
    config.scan()
    return config.make_wsgi_app()
