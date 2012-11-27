import sys

if __name__ == '__main__':
    try:
        program_name = sys.argv[0]
        app_package = sys.argv[1]
        arguments = sys.argv[2:]
        app_module = __import__(app_package)
        app = app_module.create_application()
        sys.exit(app.run(*arguments))
    except IndexError:
        print 'Usage:', program_name, 'application-module [arguments]'
        sys.exit(64)

