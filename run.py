from application import create_app
app = create_app(config = 'config')
app.run(host = '0.0.0.0')
