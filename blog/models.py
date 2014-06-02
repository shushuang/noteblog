from sqlalchemy import (
	Column,
	Integer,
	Text,
	DateTime,
	ForeignKey,
	)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	relationship,
	)
from zope.sqlalchemy import ZopeTransactionExtension
from blog import DBSession,Base

class Blog(Base):
	__tablename__='blogs'
	id = Column(Integer, primary_key = True)
	title = Column(Text, unique=True)
	content = Column(Text)
	created_time = Column(DateTime)
	last_modified_time = Column(DateTime)
	user_id = Column(Integer, ForeignKey('users.id'))
	blog_blogclass_id = relationship('Blog_BlogClass')
	tags = relationship("Blog_Tag")
	
class User(Base):
	__tablename__='users'
	id = Column(Integer, primary_key = True)
	name = Column(Text, unique = True)
	pwd = Column(Text)
	email = Column(Text)
	blogs = relationship("Blog")
	blogclasses = relationship('BlogClass')

class Tag(Base):
	__tablename__='tags'
	id = Column(Integer, primary_key = True)
	content = Column(Text, unique = True)
	
class Blog_Tag(Base):
	__tablename__='blogs_tags'
	blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key =True)
	tag_id = Column(Integer, ForeignKey('tags.id'), primary_key = True)
	tags = relationship("Tag")

class Blog_BlogClass(Base):
	__tablename__='blog_blogclass'
	blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key = True)
	blogclass_id = Column(Integer, ForeignKey('blogclasses.id'), primary_key = True)
	blog_class = relationship('BlogClass')
	
class BlogClass(Base):
	__tablename__='blogclasses'
	id = Column(Integer, primary_key = True)
	name = Column(Text, unique = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	
	
    



