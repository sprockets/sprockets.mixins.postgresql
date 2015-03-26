"""
Tests for the sprockets.mixins.postgresql package

"""
import mock
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from sprockets.clients import postgresql as _postgresql
from sprockets.mixins import postgresql


class MixinRequestHandler(postgresql.HandlerMixin):
    DBNAME = 'bar'


class AsyncMixinRequestHandler(postgresql.AsyncHandlerMixin):
    DBNAME = 'baz'


class HandlerMixinTest(unittest.TestCase):

    @mock.patch('queries.session.Session.__init__')
    def setUp(self, mock_init):
        self.mock_init = mock_init

        os.environ['BAR_HOST'] = 'db1'
        os.environ['BAR_PORT'] = '5433'
        os.environ['BAR_DBNAME'] = 'bar'
        os.environ['BAR_USER'] = 'foo'
        os.environ['BAR_PASSWORD'] = 'baz'
        self.mixin = MixinRequestHandler()
        self.mixin.initialize()

    def test_session_get_uri_value(self):
        self.assertIsInstance(getattr(self.mixin, 'bar_session'),
                              _postgresql.Session)


class AsyncHandlerMixinTest(unittest.TestCase):

    @mock.patch('queries.tornado_session.TornadoSession.__init__')
    def setUp(self, mock_init):
        self.mock_init = mock_init

        os.environ['BAZ_HOST'] = 'db2'
        os.environ['BAZ_PORT'] = '5434'
        os.environ['BAZ_DBNAME'] = 'baz'
        os.environ['BAZ_USER'] = 'qux'
        os.environ['BAZ_PASSWORD'] = 'corgie'
        self.mixin = AsyncMixinRequestHandler()
        self.mixin.initialize()

    def test_session_get_uri_value(self):
        self.assertIsInstance(getattr(self.mixin, 'baz_session'),
                              _postgresql.TornadoSession)
