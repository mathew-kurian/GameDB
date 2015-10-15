from flask import Flask, render_template
app = Flask(__name__, static_folder='public', static_url_path='/assets')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

@app.route('/')
def splash():
    return render_template('splash.jade')

if __name__ == '__main__':
    app.run()