# run_app
from deaddrop.app import flask_app

# Only execute code if ran directly
if __name__ == '__main__':
    flask_app(start_scheduler=True).run(debug=True, port=5000)
