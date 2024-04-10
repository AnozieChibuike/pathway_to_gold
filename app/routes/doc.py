from app import app
from flask import send_file
import os
from flask import Response

base_url = os.getenv('BASE_URL')


SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js" crossorigin></script>
  <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-standalone-preset.js" crossorigin></script>
    <script>
        window.onload = () => {
        window.ui = SwaggerUIBundle({
        url:'""" + f'{base_url}/swagger.json' + """',
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
      });
    };
    </script>
</body>
</html>
"""

@app.route("/docs")
def docs() -> tuple[str, int, dict[str,str]]:
    return SWAGGER_UI_HTML, 200, {"Content-Type": "text/html"}

@app.route('/swagger.json')
def swagger_json() -> Response:
    return send_file('swagger_config.json', mimetype='application/json')


