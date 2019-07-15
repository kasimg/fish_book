"""
Created by kasim on 2019/7/9 12:53
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=True)
