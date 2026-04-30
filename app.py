from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

app = Dash(__name__)
server = app.server

# Data
data = [
    {"date": "2026-01-02", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-01-08", "people": ["Thoby", "Paige", "Maxime"], "location": "West 4th", "future": False},
    {"date": "2026-01-10", "people": ["Thoby", "Victor"], "location": "West 4th", "future": False},
    {"date": "2026-01-12", "people": ["Thoby", "Leo", "Danny"], "location": "Robson", "future": False},
    {"date": "2026-01-14", "people": ["Thoby", "Spencer", "Aiden"], "location": "Robson", "future": False},
    {"date": "2026-01-23", "people": [], "location": "West 4th", "future": False},
    {"date": "2026-01-27", "people": ["Thoby", "Jake", "Danny"], "location": "West 4th", "future": False},
    {"date": "2026-02-02", "people": ["Thoby", "Carrington"], "location": "North Van", "future": False},
    {"date": "2026-02-16", "people": ["Thoby", "Leo", "Victor"], "location": "West 4th", "future": False},
    {"date": "2026-02-18", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-02-26", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-03-07", "people": ["Reagan"], "location": "West 4th", "future": False},
    {"date": "2026-03-08", "people": ["Danny", "Carrington", "Isabelle"], "location": "North Van", "future": False},
    {"date": "2026-03-15", "people": ["Kathleen", "Logan", "Josh"], "location": "Kerrisdale", "future": False},
    {"date": "2026-04-03", "people": ["Carrington"], "location": "North Van", "future": False},
    {"date": "2026-04-15", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-04-19", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-04-29", "people": [], "location": "West 4th", "future": False},
    {"date": "2026-05-04", "people": ["Carrington"], "location": "North Van", "future": True},
    {"date": "2026-05-11", "people": ["Paige"], "location": "West 4th", "future": True},
]

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])
df["group_size"] = df["people"].apply(lambda x: len(x) + 1)
df["companions"] = df["people"].apply(lambda x: ", ".join(x) if x else "Solo")
df["date_str"] = df["date"].dt.strftime("%b %-d")

location_colors = {
    "West 4th": "#2ecc71",
    "Robson": "#e74c3c",
    "North Van": "#3498db",
    "Kerrisdale": "#f39c12",
}

BACKGROUND = "#0d1117"
CARD_BG = "#161b22"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#2ecc71"

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("2026 Soup Series", style={
            "margin": "0", "fontSize": "2rem", "fontWeight": "700",
            "fontFamily": "'Georgia', serif", "color": TEXT, "letterSpacing": "-0.5px"
        }),
    ], style={"padding": "32px 32px 16px", "borderBottom": "1px solid #21262d"}),

    # Stats row
    html.Div(id="stats-row", style={
        "display": "flex", "gap": "16px", "padding": "20px 32px",
        "flexWrap": "wrap"
    }),

    # Controls
    html.Div([
        html.Div([
            html.Label("View", style={"color": MUTED, "fontSize": "0.75rem", "fontFamily": "monospace", "marginBottom": "6px", "display": "block"}),
            dcc.Dropdown(
                id="chart-select",
                options=[
                    {"label": "Timeline", "value": "timeline"},
                    {"label": "By Location", "value": "location"},
                    {"label": "By Person", "value": "person"},
                ],
                value="timeline",
                clearable=False,
                style={"width": "180px"},
            ),
        ]),
        html.Div([
            html.Label("Location", style={"color": MUTED, "fontSize": "0.75rem", "fontFamily": "monospace", "marginBottom": "6px", "display": "block"}),
            dcc.Dropdown(
                id="location-filter",
                options=[{"label": "All Locations", "value": "all"}] +
                        [{"label": l, "value": l} for l in sorted(df["location"].unique())],
                value="all",
                clearable=False,
                style={"width": "200px"},
            ),
        ]),
    ], style={"display": "flex", "gap": "16px", "padding": "0 32px 20px", "alignItems": "flex-end"}),

    # Chart
    html.Div([
        dcc.Graph(id="main-chart", style={"height": "380px"},
                  config={"displayModeBar": False})
    ], style={"padding": "0 16px 32px"}),

], style={
    "backgroundColor": BACKGROUND,
    "minHeight": "100vh",
    "fontFamily": "'Helvetica Neue', sans-serif",
    "color": TEXT,
})


def stat_card(label, value, color=ACCENT):
    return html.Div([
        html.Div(str(value), style={
            "fontSize": "2rem", "fontWeight": "700", "color": color,
            "fontFamily": "'Georgia', serif", "lineHeight": "1"
        }),
        html.Div(label, style={
            "fontSize": "0.72rem", "color": MUTED, "marginTop": "4px",
            "fontFamily": "monospace", "textTransform": "uppercase", "letterSpacing": "0.05em"
        }),
    ], style={
        "backgroundColor": CARD_BG,
        "border": "1px solid #21262d",
        "borderRadius": "8px",
        "padding": "16px 20px",
        "minWidth": "100px",
    })


@callback(Output("stats-row", "children"), Input("location-filter", "value"))
def update_stats(loc):
    filtered = df if loc == "all" else df[df["location"] == loc]
    past = filtered[~filtered["future"]]
    total = len(past)
    solo = len(past[past["companions"] == "Solo"])
    all_people = [p for row in past["people"] for p in row]
    top = max(set(all_people), key=all_people.count) if all_people else "—"
    fav_loc = past["location"].value_counts().idxmax() if total > 0 else "—"
    return [
        stat_card("Total Bowls", total),
        stat_card("Solo Visits", solo, "#8b949e"),
        stat_card("Most With", top, "#3498db"),
        stat_card("Top Spot", fav_loc, "#f39c12"),
    ]


@callback(Output("main-chart", "figure"),
          Input("chart-select", "value"),
          Input("location-filter", "value"))
def update_chart(chart_type, loc):
    filtered = df if loc == "all" else df[df["location"] == loc]
    past = filtered[~filtered["future"]]

    plot_cfg = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="'Helvetica Neue', sans-serif"),
        margin=dict(l=20, r=20, t=40, b=40),
    )

    if chart_type == "timeline":
        fig = go.Figure()

        for location, color in location_colors.items():
            sub = past[past["location"] == location]
            if sub.empty:
                continue

            sizes = sub["group_size"].apply(lambda s: 10 + s * 6)

            hover = sub.apply(
                lambda r: (
                    f"<b>{r['date_str']}</b><br>"
                    f"📍 {r['location']}<br>"
                    f"👥 me" + (f", {r['companions']}" if r['companions'] != 'Solo' else "")
                ),
                axis=1
            )

            fig.add_trace(go.Scatter(
                x=sub["date"],
                y=[0] * len(sub),
                mode="markers",
                name=location,
                marker=dict(
                    size=sizes,
                    color=color,
                    opacity=0.85,
                    line=dict(width=2, color=BACKGROUND),
                ),
                text=hover,
                hovertemplate="%{text}<extra></extra>",
            ))

        # Future visit
        future = filtered[filtered["future"]]
        if not future.empty:
            hover_future = future.apply(
                lambda r: (
                    f"<b>{r['date_str']} ⭐ upcoming</b><br>"
                    f"📍 {r['location']}<br>"
                    f"👥 me" + (f", {r['companions']}" if r['companions'] != 'Solo' else "")
                ),
                axis=1
            )
            fig.add_trace(go.Scatter(
                x=future["date"],
                y=[0] * len(future),
                mode="markers",
                name="Upcoming",
                marker=dict(
                    size=future["group_size"].apply(lambda s: 10 + s * 6),
                    color="#f39c12",
                    symbol="star",
                    opacity=0.9,
                    line=dict(width=2, color=BACKGROUND),
                ),
                text=hover_future,
                hovertemplate="%{text}<extra></extra>",
            ))

        fig.update_layout(
            **plot_cfg,
            xaxis=dict(gridcolor="#21262d", zeroline=False, showline=True, linecolor="#21262d"),
            yaxis=dict(visible=False, range=[-1, 1]),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#21262d", borderwidth=1),
            hovermode="closest",
        )

        fig.add_annotation(
            text="dot size = group size",
            xref="paper", yref="paper",
            x=1, y=1.08, showarrow=False,
            font=dict(size=11, color=MUTED),
            xanchor="right"
        )

    elif chart_type == "location":
        counts = past["location"].value_counts().reset_index()
        counts.columns = ["location", "count"]
        colors = [location_colors.get(l, "#8b949e") for l in counts["location"]]
        fig = go.Figure(go.Bar(
            x=counts["location"], y=counts["count"],
            marker_color=colors,
            text=counts["count"], textposition="outside",
            hoverinfo="x+y",
        ))
        fig.update_layout(**plot_cfg,
                          xaxis=dict(gridcolor="#21262d"),
                          yaxis=dict(gridcolor="#21262d", zeroline=False))

    elif chart_type == "person":
        all_people = [p for row in past["people"] for p in row]
        if not all_people:
            fig = go.Figure()
            fig.update_layout(**plot_cfg)
        else:
            counts = Counter(all_people).most_common()
            names, vals = zip(*counts)
            fig = go.Figure(go.Bar(
                x=list(vals), y=list(names), orientation="h",
                marker_color=ACCENT,
                text=list(vals), textposition="outside",
                hoverinfo="y+x",
            ))
            fig.update_layout(**plot_cfg,
                              xaxis=dict(gridcolor="#21262d", zeroline=False),
                              yaxis=dict(gridcolor="#21262d", autorange="reversed"),
                              height=max(300, len(names) * 36))

    return fig


if __name__ == "__main__":
    app.run(debug=True)
