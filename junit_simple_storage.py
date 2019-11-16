#!/usr/bin/env python3

import connexion

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yml')

@app.route('/')
def hello():
    return 'Hello junit simple storage'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)