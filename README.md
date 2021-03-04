# Graph File Generator

This tool helps convert CSV/TSV file data with graph edges to a PDF/PNG file. More details about data format can be found in the demo link.
A directional graph/network can be converted into a hierarchical graph. The tool uses PyDot, Graphviz and NetworkX.

Demo : https://graph-visualizer-pdf.herokuapp.com/

Requires Recaptcha setup (https://www.google.com/recaptcha). Set the secret key to the RECAPTCHA_KEY environment variable and modify the site key in graph_main.py and index.html.

To install,

> sudo apt install graphviz

> pip install -r requirements.txt

To run,
> python graph_main.py
