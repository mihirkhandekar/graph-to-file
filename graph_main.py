import networkx as nx
from flask import Flask, redirect, render_template, request, send_file, url_for
from flask_wtf import Form
from wtforms import TextField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        graph_data = request.form['graph_data']
        format = request.form['format']
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
        parent = parent_child_relation[0]
        child = parent_child_relation[1]
        G.add_edge(parent, child)

    A = nx.nx_agraph.to_agraph(G)

    A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=.1 -Gfontsize=10 -Granksep=2')
    if format == 'PDF':
        filename = 'graph.pdf'
    else:
        filename = 'graph.png'
    A.draw(filename)
    return filename


if __name__ == '__main__':
    app.run('0.0.0.0')
