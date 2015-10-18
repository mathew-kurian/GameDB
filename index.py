# pip3 install pyjade
# pip3 install Flask


from flask import Flask, render_template, redirect

app = Flask(__name__, static_folder='public', static_url_path='/assets')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True


@app.route('/')
def index():
    return render_template('index.jade', assets='assets/')


@app.route('/index.html')
def index():
    return redirect('/', code=302)


@app.route('/about')
def about():
    return render_template('about.jade', assets='assets/')


@app.route('/games')
def games():
    return render_template('games.jade', assets='assets/')


@app.route('/releases')
def releases():
    return render_template('releases.jade', assets='assets/')


@app.route('/publishers')
def publishers():
    return render_template('publishers.jade', assets='assets/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
