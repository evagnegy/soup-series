from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import os


#port = os.environ.get("APP_PORT", 39999)
#prefix = os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/")
#path_prefix = os.environ.get("APP_CONTEXT_ROOT", f"{prefix}proxy/{port}/")
#app =  Dash(__name__, requests_pathname_prefix=path_prefix, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app = Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server
 
app.index_string = """
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>2026 Soup Series</title>
{%favicon%}
{%css%}
<style>
  .dash-dropdown .Select-control,
  .dash-dropdown .VirtualizedSelect-control,
  .dash-dropdown [class$="-control"],
  .dash-dropdown [class*="-control"] {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    min-height: 44px !important;
    box-shadow: none !important;
  }
  .dash-dropdown .Select-control:hover,
  .dash-dropdown [class*="-control"]:hover { border-color: #8b949e !important; }
  .dash-dropdown .Select-value-label,
  .dash-dropdown .Select-placeholder,
  .dash-dropdown [class*="-singleValue"],
  .dash-dropdown [class*="-placeholder"] { color: #e6edf3 !important; }
  .dash-dropdown [class*="-placeholder"] { color: #8b949e !important; }
  .dash-dropdown .Select-arrow { border-top-color: #8b949e !important; }
  .dash-dropdown [class*="-indicatorSeparator"] { background-color: #30363d !important; }
  .dash-dropdown [class*="-indicatorContainer"] svg,
  .dash-dropdown [class*="-dropdownIndicator"] svg { fill: #8b949e !important; }
  .dash-dropdown .Select-menu-outer,
  .dash-dropdown [class*="-menu"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    z-index: 999 !important;
  }
  .dash-dropdown [class*="-MenuList"],
  .dash-dropdown [class*="-menuList"] { background-color: #161b22 !important; }
  .dash-dropdown .Select-option,
  .dash-dropdown [class*="-option"] { background-color: #161b22 !important; color: #e6edf3 !important; }
  .dash-dropdown .Select-option:hover,
  .dash-dropdown .Select-option.is-focused,
  .dash-dropdown [class*="-option"]:hover,
  .dash-dropdown [class*="-option--is-focused"] { background-color: #21262d !important; }
  .dash-dropdown .Select-option.is-selected,
  .dash-dropdown [class*="-option--is-selected"] { background-color: #2d333b !important; }
  .dash-dropdown [class*="-Input"] input,
  .dash-dropdown .Select-input input { color: #e6edf3 !important; background: transparent !important; }
</style>
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""
 

data = [
    {"date": "2026-01-02", "people": ["Thoby"], "location": "West 4th", "future": False},
    {"date": "2026-01-08", "people": ["Thoby", "Paige", "Maxime"], "location": "West 4th", "future": False},
    {"date": "2026-01-10", "people": ["Thoby", "Victor"], "location": "West 4th", "future": False},
    {"date": "2026-01-12", "people": ["Thoby", "Leo", "Danny"], "location": "Robson", "future": False},
    {"date": "2026-01-14", "people": ["Thoby", "Spencer", "Aiden"], "location": "Robson", "future": False, "note": "spencers first time!"},
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
    {"date": "2026-05-04", "people": ["Carrington"], "location": "North Van", "future": False},
    {"date": "2026-05-11", "people": ["Paige"], "location": "West 4th", "future": False, "note": "thobs guest appearance"},
    {"date": "2026-05-15", "people": ["Thoby"], "location": "West 4th", "future": True},
]
 
df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])
df["group_size"] = df["people"].apply(lambda x: len(x) + 1)
df["companions"] = df["people"].apply(lambda x: ", ".join(x) if x else "Solo")
df["date_str"] = df["date"].dt.strftime("%b %-d")
if "note" not in df.columns:
    df["note"] = None
 
location_colors = {
    "West 4th": "#2ecc71",
    "Robson": "#e74c3c",
    "North Van": "#3498db",
    "Kerrisdale": "#f39c12",
}
 
location_emoji = {
    "West 4th": "🍜",
    "Robson": "🏢",
    "North Van": "⛴️",
    "Kerrisdale": "🚲",
}
 
BACKGROUND = "#0d1117"
CARD_BG = "#161b22"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#2ecc71"
 
PAD = "clamp(12px, 4vw, 32px)"
 
app.layout = html.Div([
    html.Div([
        html.H1("2026 Soup Series", style={
            "margin": "0", "fontSize": "2rem", "fontWeight": "700",
            "fontFamily": "'Georgia', serif", "color": TEXT, "letterSpacing": "-0.5px"
        }),
    ], style={"padding": f"32px {PAD} 16px", "borderBottom": "1px solid #21262d"}),
 
    html.Div(id="stats-row", style={
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fit, minmax(120px, 1fr))",
        "gap": "12px",
        "padding": f"20px {PAD}",
    }),
 
    html.Div([
        html.Div([
            html.Label("View", style={
                "color": MUTED, "fontSize": "0.75rem", "fontFamily": "monospace",
                "marginBottom": "6px", "display": "block"
            }),
            dcc.Dropdown(
                id="chart-select",
                options=[
                    {"label": "Timeline", "value": "timeline"},
                    {"label": "By Location", "value": "location"},
                    {"label": "By Person", "value": "person"},
                ],
                value="timeline",
                clearable=False,
                style={"width": "100%"},
            ),
        ], style={"width": "180px", "minWidth": "140px", "flex": "0 1 180px"}),
        html.Div([
            html.Label("Location", style={
                "color": MUTED, "fontSize": "0.75rem", "fontFamily": "monospace",
                "marginBottom": "6px", "display": "block"
            }),
            dcc.Dropdown(
                id="location-filter",
                options=[{"label": "All Locations", "value": "all"}] +
                        [{"label": l, "value": l} for l in sorted(df["location"].unique())],
                value="all",
                clearable=False,
                style={"width": "100%"},
            ),
        ], style={"width": "200px", "minWidth": "140px", "flex": "0 1 200px"}),
    ], style={
        "display": "flex",
        "gap": "16px",
        "padding": f"0 {PAD} 20px",
        "alignItems": "flex-end",
        "flexWrap": "wrap",
    }),
 
    html.Div([
        dcc.Graph(
            id="main-chart",
            style={"height": "clamp(260px, 50vw, 380px)"},
            config={"displayModeBar": False},
        )
    ], style={"padding": f"0 8px 32px"}),
 
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
    })
 
 
def build_hover(r):
    """Build hover text for a row, appending a note line if present."""
    people_str = f", {r['companions']}" if r['companions'] != 'Solo' else ""
    lines = [
        f"<b>{r['date_str']}</b>",
        f"📍 {r['location']}",
        f"👥 me{people_str}",
    ]
    if pd.notna(r.get("note")) and r["note"]:
        lines.append(f"✱ {r['note']}")
    return "<br>".join(lines)
 
 
def build_hover_future(r):
    people_str = f", {r['companions']}" if r['companions'] != 'Solo' else ""
    lines = [
        f"<b>{r['date_str']} 🔮 upcoming</b>",
        f"📍 {r['location']}",
        f"👥 me{people_str}",
    ]
    if pd.notna(r.get("note")) and r["note"]:
        lines.append(f"✱ {r['note']}")
    return "<br>".join(lines)
 
 
@callback(Output("stats-row", "children"), Input("location-filter", "value"))
def update_stats(loc):
    filtered = df if loc == "all" else df[df["location"] == loc]
    past = filtered[~filtered["future"]]
    total = len(past)
    solo = len(past[past["companions"] == "Solo"])
    all_people = [p for row in past["people"] for p in row]
    top = max(set(all_people), key=all_people.count) if all_people else "—"
    fav_loc = past["location"].value_counts().idxmax() if total > 0 else "—"
    start = pd.Timestamp(past["date"].dt.year.min(), 1, 1) if total > 0 else pd.Timestamp("2026-01-01")
    weeks_elapsed = max((pd.Timestamp.today() - start).days / 7, 1)
    per_week = round(total / weeks_elapsed, 1)
    return [
        stat_card("Total Bowls", total),
        stat_card("Per Week", per_week, ACCENT),
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
    )
 
    if chart_type == "timeline":
        fig = go.Figure()
 
        for location, color in location_colors.items():
            sub = past[past["location"] == location]
            if sub.empty:
                continue
            emoji = location_emoji.get(location, "🍜")
            hover = sub.apply(build_hover, axis=1)
 
            fig.add_trace(go.Scatter(
                x=sub["date"].tolist(),
                y=[0] * len(sub),
                mode="markers+text",
                name=emoji,
                marker=dict(color=color, size=1, opacity=0),
                text=[emoji] * len(sub),
                textfont=dict(size=sub["group_size"].apply(lambda s: 16 + s * 4).tolist()),
                textposition="middle center",
                cliponaxis=False,
                customdata=hover,
                hovertemplate="%{customdata}<extra></extra>",
                showlegend=False,
            ))
 
        future = filtered[filtered["future"]]
        if not future.empty:
            hover_future = future.apply(build_hover_future, axis=1)
            fig.add_trace(go.Scatter(
                x=future["date"].tolist(),
                y=[0] * len(future),
                mode="markers+text",
                name="🔮",
                marker=dict(color="#f39c12", size=1, opacity=0),
                text=["🔮"] * len(future),
                textfont=dict(size=future["group_size"].apply(lambda s: 16 + s * 4).tolist()),
                textposition="middle center",
                cliponaxis=False,
                customdata=hover_future,
                hovertemplate="%{customdata}<extra></extra>",
                showlegend=False,
            ))
 
        # Manual emoji legend via annotations
        all_locations = [l for l in location_emoji if not past[past["location"] == l].empty]
        future_present = not filtered[filtered["future"]].empty
        legend_entries = [(l, location_emoji[l]) for l in all_locations]
        if future_present:
            legend_entries.append(("Upcoming", "🔮"))
 
        for i, (label, emoji) in enumerate(legend_entries):
            fig.add_annotation(
                text=f"{emoji} {label}",
                xref="paper", yref="paper",
                x=1.01, y=1.0 - i * 0.12,
                showarrow=False,
                font=dict(size=12, color=TEXT),
                xanchor="left",
                align="left",
            )
 
        fig.update_layout(
            **plot_cfg,
            xaxis=dict(type="date", gridcolor="#21262d", zeroline=False, showline=True, linecolor="#21262d"),
            yaxis=dict(visible=False, range=[-1, 1]),
            showlegend=False,
            margin=dict(l=20, r=130, t=20, b=40),
            hovermode="closest",
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
                          margin=dict(l=20, r=20, t=40, b=40),
                          xaxis=dict(gridcolor="#21262d"),
                          yaxis=dict(gridcolor="#21262d", zeroline=False))
 
    elif chart_type == "person":
        all_people = [p for row in past["people"] for p in row]
        if not all_people:
            fig = go.Figure()
            fig.update_layout(**plot_cfg, margin=dict(l=20, r=20, t=40, b=40))
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
                              margin=dict(l=20, r=20, t=40, b=40),
                              xaxis=dict(gridcolor="#21262d", zeroline=False),
                              yaxis=dict(gridcolor="#21262d", autorange="reversed"),
                              height=max(300, len(names) * 36))
 
    return fig


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(port=port, host='0.0.0.0')