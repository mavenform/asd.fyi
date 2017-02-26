from flask import Flask, request, redirect
import os
import redis

app = Flask(__name__) 
chars = [str(x) for x in range(10)] + [chr(x) for x in range(97, 123)]
r = redis.from_url(os.environ.get("REDIS_URL"))

html  = '''
<style>
body{font-family:monospace;}
</style>
<script src="https://cdn.jsdelivr.net/clipboard.js/1.6.0/clipboard.min.js"></script>
<script>new Clipboard('input');</script>
<p>asd.fyi - share text.</p>
<form action="/" method="post"><textarea name="t" rows="20" cols="80"></textarea><br/><br/><input type="submit" value="submit and copy to clipboard" 
	data-clipboard-text="www.asd.fyi" /></form>
'''

def getid():
	return r.incr("id", 1)

def n_to_s(n):
	s = ""
	while n:
		s = s + chars[n % len(chars)]
		n = n // len(chars)
	return s

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path>")
def paste(path):
	if path:
		return "<pre>%s</pre>" % (r.get(path).decode("utf-8"),)
	elif request.form.get("t"):	
		t = request.form.get("t")
		curid = n_to_s(getid())
		r.set(curid, t)
		return redirect("/%s" % (curid,))
	return html

if __name__ == '__main__':
	app.run()
