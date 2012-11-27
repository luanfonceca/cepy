-----------------------
 flask-heroku-skeleton
-----------------------

.. class:: align-center

*Flask and Heroku -- they taste good together!*


This is a simple skeleton that you can clone and get a `Flask`_ application
that will work within the `Heroku`_ environment.  Use the following recipe
to create a brand new application:

1. Clone the repo into a new directory
2. Rename the *myapp* subdirectory to your application name
3. Edit *setup.py* and
     a. change ``package_name`` to the name of your package
     b. edit the commented out keywords in the call to ``setup``

4. Edit *Procfile* and change ``myapp`` to your package name
5. Install all of the requirements with `pip`_
   ::

      shell$ pip -q install -r requirements.txt
      shell$ pip -q install -r docs/test-requirements
      shell$ pip -q install -r docs/dev-requirements

6. edit the tests and change *myapp* to your package name
7. run the tests with `nosetests`_
8. *git commit* your changes

You're application is set up and ready to run with the Heroku python stack.

.. _Flask: http://flask.pocoo.org/
.. _Heroku: http://www.heroku.com/
.. _pip: http://www.pip-installer.org/
.. _nosetests: http://readthedocs.org/docs/nose/

