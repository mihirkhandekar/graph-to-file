import json
import os

import networkx as nx
import pydot

import requests
from flask import Flask, redirect, render_template, request, send_file, url_for
from flask_recaptcha import ReCaptcha
from flask_wtf import Form
from networkx.drawing.nx_pydot import to_pydot

app = Flask(__name__)

app.config['SECRET_KEY'] = 'our very hard to guess secretfir'

app.config.update({'RECAPTCHA_ENABLED': True,
                   'RECAPTCHA_SITE_KEY':
                       '6LeV1XAaAAAAAABdGY5EryeEMH3CJ_c1yYipElJN',
                   'RECAPTCHA_SECRET_KEY':
                       os.environ['RECAPTCHA_KEY']})
recaptcha = ReCaptcha(app=app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        graph_data = request.form['graph_data']
        format = request.form['format']
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret':
                                os.environ['RECAPTCHA_KEY'],
                                'response':
                                request.form['g-recaptcha-response']})

        google_response = json.loads(r.text)
        print('Captcha response: ', google_response)

        if google_response['success']:
            filename = draw_graph(graph_data, format)
            return send_file(filename, as_attachment=True)

    return render_template('index.html')


def draw_graph(graph_content, format):
    parent_child_relations = []
    for line in graph_content.split('\n'):
        if ',' in line.strip():
            split = line.split(',')
            parent_child_relations.append([split[0].strip(), split[1].strip()])
        elif '\t' in line.strip():
            split = line.split('\t')
            parent_child_relations.append([split[0].strip(), split[1].strip()])

    G = nx.DiGraph()

    for parent_child_relation in parent_child_relations:
        parent, child = parent_child_relation
        if parent == 'graph':
            parent = 'graph_'
        if child == 'graph':
            child = 'graph_'
        G.add_edge(parent, child)

    A = nx.drawing.nx_pydot.to_pydot(G)  # nx.nx_agraph.to_agraph(G)

    A.set_size(120)
    A.set_ranksep(3)
    A.set_fontsize(20)

    if format == 'PDF':
        filename = 'graph.pdf'
        A.write_pdf(filename)
    else:
        filename = 'graph.png'
        A.write_png(filename)
    return filename


if __name__ == '__main__':
    app.run('0.0.0.0')
