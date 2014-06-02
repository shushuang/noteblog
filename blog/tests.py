import unittest
from pyramid import testing
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('blog')

import unittest
import transaction

from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from blog import DBSession
    from blog.models import(
		)
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind = engine)
    with transaction.manager:
        model = Page(name = 'FrontPage', data='')
        DBSession.add(model)
    return DBSession
def _registerRoutes(config):
    config.add_route('', '')	
class ViewTests(unittest.TestCase):
    def setUp(self):
        testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from blog.views import my_view
        request = testing.DummyRequest()
        response = my_view(request)
        self.assertEqual(response['project'], 'blog')

