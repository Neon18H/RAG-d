import os, requests
from flask import Flask, request, render_template_string

API_URL = os.getenv("API_URL", "http://localhost:8010")
app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>RAG vía API (OpenAI/Gemini)</title>
<h2>RAG vía API (OpenAI/Gemini)</h2>
<form method="post">
  <input name="q" placeholder="Escribe tu pregunta" style="width:60%"/>
  <button type="submit">Preguntar</button>
</form>
{% if answer %}
  <h3>Respuesta</h3>
  <div><pre style="white-space:pre-wrap">{{ answer }}</pre></div>
  <h4>Pasajes</h4>
  <ul>
    {% for p in passages %}
      <li><b>{{ p.id }}</b>: {{ p.text[:200] }}...</li>
    {% endfor %}
  </ul>
{% endif %}
"""

@app.route('/', methods=['GET','POST'])
def index():
    answer, passages = None, []
    if request.method == 'POST':
        q = request.form.get('q','').strip()
        if q:
            r = requests.post(f"{API_URL}/ask", json={"question": q}, timeout=300)
            r.raise_for_status()
            data = r.json()
            answer = data.get('answer')
            passages = data.get('passages', [])
    return render_template_string(TEMPLATE, answer=answer, passages=passages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))
