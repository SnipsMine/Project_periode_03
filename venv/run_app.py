from lib.app_setup import app


if __name__ == '__main__':
    # setting debug on True will restart the server on each change
    app.debug = True
    app.run()
