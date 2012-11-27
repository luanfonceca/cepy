import cep
import testing


class ApplicationDefaultTest(testing.TestCase):
    """Validate the application default configuration."""
    def test_host_defaults_to_all(self):
        app = cep.create_application()
        self.assertEqual(app.config['HOST'], '0.0.0.0')

    def test_port_defaults_to_5000(self):
        app = cep.create_application()
        self.assertEqual(app.config['PORT'], 5000)

    def test_debug_defaults_to_false(self):
        app = cep.create_application()
        self.assertEqual(app.config['DEBUG'], False)
        self.assertEqual(app.debug, False)

    def test_secret_key_is_generated(self):
        app = cep.create_application()
        key = app.config['SECRET_KEY']
        self.assertIsNotNone(key)
        self.assertEqual(len(key), 24)


class ApplicationRunTests(testing.TestCase):
    """Verify aspects of creating and running the application."""
    @testing.patch('cep.flaskapp.Application')
    def test_create_application_curries_arguments(self, app_class):
        cep.create_application()
        app_class.assert_called_with()
        cep.create_application(1, 2, 3)
        app_class.assert_called_with(1,2,3)
        cep.create_application(1, 2, three=3)
        app_class.assert_called_with(1, 2, three=3)

    @testing.patch('flask.Flask.run')
    def test_run_curries_arguments(self, flask_run):
        inst = cep.create_application()
        inst.run()
        flask_run.assert_called_with(inst, host='0.0.0.0', port=5000,
                debug=False)
        inst.run(42, foo='bar')
        flask_run.assert_called_with(inst, 42, host='0.0.0.0', port=5000,
                debug=False, foo='bar')

    @testing.patch('flask.Flask.run')
    def test_run_keywords_override_defaults(self, flask_run):
        inst = cep.create_application()
        inst.run(debug=True, host='127.0.0.1', port=6543)
        flask_run.assert_called_with(inst, host='127.0.0.1', port=6543,
                debug=True)


class ConfigFileTests(testing.TestCase):
    """I test application configuration file processing."""
    @testing.patch('flask.Config.from_envvar')
    def test_config_file_from_envvar_is_read(self, from_envvar):
        inst = cep.create_application()
        from_envvar.assert_called_with('APP_CONFIG', silent=True)
        inst = cep.create_application(config_envvar='CUSTOM_NAME')
        from_envvar.assert_called_with('CUSTOM_NAME', silent=True)

