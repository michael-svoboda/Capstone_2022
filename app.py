import dash
import dash_labs as dl
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Pages",
    ),
    brand="Oil and Gas Data App",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    
    [navbar, dl.plugins.page_container],    
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)