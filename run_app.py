import os

from api.exampleAPI import app
from api.exampleAPI import create_table

if __name__ == '__main__':
    create_table()
    app.debug = True
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)