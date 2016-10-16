from flask import Flask, request
from flask import render_template
from mandelbrot import *

app = Flask(__name__)

# Simple static content on index.
@app.route('/')
def index():
    return 'Index page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name)

@app.route('/image')
def image():
	return ''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route ('/mandelbrot')
def mandelbrot():
	x1 = int(request.args.get('x1'))
	y1 = int(request.args.get('y1'))
	x2 = int(request.args.get('x2'))
	y2 = int(request.args.get('y2'))
	width = int(request.args.get('width'))
	it = int(request.args.get('it'))
	fileName = "mandelbrot-"+str(x1)+"_"+str(x2)+"-"+str(x2)+"_"+str(y2)+"-w"+str(width)+"-it"+str(it)+".png"
	mandelbrotData = {'imageFile': fileName, 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'width': width, 'it': it}
	renderizaMandelbrot(x1,y1,x2,y2,width,it, fileName)
	return render_template('mandelbrot.html', mandelbrotData = mandelbrotData)
