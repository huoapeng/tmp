from myapi import create_app

if __name__ == '__main__':
    app = create_app('config.dev')
    app.run()