from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'graph.db'

def get_graph():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT name FROM nodes')
    nodes = [row[0] for row in c.fetchall()]

    c.execute('SELECT from_node, to_node, distance FROM edges')
    edges = c.fetchall()
    conn.close()

    graph = {node: {} for node in nodes}
    for from_node, to_node, distance in edges:
        graph[from_node][to_node] = {'distance': distance}
    return graph

@app.route('/')
def index():
    graph = get_graph()
    return render_template('index.html', graph=graph)

@app.route('/add_node', methods=['POST'])
def add_node():
    node_name = request.form.get('node_name').strip()
    if node_name:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO nodes (name) VALUES (?)', (node_name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # node already exists
        conn.close()
    return redirect(url_for('index'))

@app.route('/add_edge', methods=['POST'])
def add_edge():
    from_node = request.form.get('from_node').strip()
    to_node = request.form.get('to_node').strip()
    weight = request.form.get('weight').strip()

    try:
        weight = float(weight)
    except ValueError:
        return redirect(url_for('index'))

    if from_node and to_node:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        # Ensure nodes exist
        for node in [from_node, to_node]:
            c.execute('INSERT OR IGNORE INTO nodes (name) VALUES (?)', (node,))
        # Add edge
        c.execute('INSERT INTO edges (from_node, to_node, distance) VALUES (?, ?, ?)',
                  (from_node, to_node, weight))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
