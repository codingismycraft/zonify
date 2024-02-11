"""Simple server to display the encolosing Geo Polygons for post code."""

from flask import Flask

import utils.constants as constants
import utils.polygons as polygons

app = Flask(__name__)


@app.route("/polygon/<post_code>")
def get_polygon(post_code):
    """Returns the enclosing polygon for the passed in post code."""
    return polygons.make_map(post_code)


if __name__ == '__main__':
    print(f"Starting the zomify server in port: {constants.PORT}")
    app.run(host="0.0.0.0", port=constants.PORT, debug=True)
