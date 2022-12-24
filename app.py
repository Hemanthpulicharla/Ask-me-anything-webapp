import os
from io import StringIO
import sys
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = "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"

with open('prompt.txt') as f:
    PROMPT = f.read()
STDOUT = sys.stdout


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    if(request.form['action'] == 'images'):
      query=request.form["animal"]
      response = openai.Image.create(
            prompt=query,
              n=1,
              size="512x512")
      image_url = response['data'][0]['url']
      return render_template("index.html",image=image_url)
    question = request.form["animal"]
    if(request.form['action']=='names'):
     	if question == "":
     		pass
     	prompt = f'{PROMPT} {question}\nAnswer:\n```'
     	response = openai.Completion.create(model="text-davinci-002",prompt=prompt,temperature=0,max_tokens=512,stop='```',)
     	code = response.choices[0].text.strip()
     	indented_code = '\n'.join([f'\t{line}' for line in code.splitlines()])
     	s=f'Generated Code at my end:\n{indented_code}'
     	sys.stdout=output = StringIO()
     	exec(code)
     	sys.stdout=STDOUT
     	s2=output.getvalue()
     	printer="Answer after excuting the code above: "+str(s2)
     	return render_template("index.html",printer=printer,code=s)
  return render_template("index.html")
if __name__=='__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
