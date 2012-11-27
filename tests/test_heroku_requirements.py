from __future__ import with_statement
import cep
import os
import flask
import testing


@testing.save_and_restore_environ
class HerokuEnvironmentTest(testing.TestCase):
    """
    Tests related to the heroku python environment.

    The Heroku stack communicates the run time parameters via environment
    variables with well-known (and documented) names.  This test ensures that
    the application is indeed honoring the environment variables so that there
    are no undue surprises at deployment time.
    """
    def test_host_envvar(self):
        os.environ['HOST'] = 'server.company.com'
        app = cep.create_application()
        self.assertEqual(app.config['HOST'], 'server.company.com')
        with app.test_request_context('/'):
            self.assertEqual(flask.current_app.config['HOST'],
                    'server.company.com')

    def test_port_envvar(self):
        os.environ['PORT'] = '6543'
        app = cep.create_application()
        self.assertEqual(app.config['PORT'], 6543)
        with app.test_request_context('/'):
            self.assertEqual(flask.current_app.config['PORT'], 6543)

    def test_debug_flag_from_environment(self):
        os.environ['DEBUG'] = 'true'
        app = cep.create_application()
        self.assertEqual(app.config['DEBUG'], True)
        self.assertEqual(app.debug, True)
        with app.test_request_context('/'):
            self.assertEqual(flask.current_app.config['DEBUG'], True)
            self.assertEqual(flask.current_app.debug, True)

    @testing.patch('flask.Flask.run')
    def test_environment_args(self, flask_run):
        os.environ['HOST'] = 'server.company.com'
        os.environ['PORT'] = '6543'
        os.environ['DEBUG'] = 'True'
        app = cep.create_application()
        app.run()
        flask_run.assert_called_once_with(app, host='server.company.com',
                port=6543, debug=True)

