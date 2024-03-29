from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dashboard.src.data.data_loader import DataSource
from dashboard.src.components.styles import loss_type_dropdown_styles


def render(
      app: Dash,
      source: DataSource,
      dropdown_id: str,
      ) -> html.Div:

    @app.callback(
        Output(dropdown_id, "value"),
        Input(dropdown_id, "value"),
    )
    def select_loss_type(selected_value: str) -> str:
        return selected_value

    return html.Div(
        children=[
            html.H5('Loss Type'),
            dcc.Dropdown(
                id=dropdown_id,
                options=[{"label": loss_type, "value": loss_type} for loss_type in source.LOSS_TYPE],
                value=source.LOSS_TYPE[0], # default value is 'total'
                style=loss_type_dropdown_styles['level_2'],
            ),
        ],
        style=loss_type_dropdown_styles['level_1'],
    )