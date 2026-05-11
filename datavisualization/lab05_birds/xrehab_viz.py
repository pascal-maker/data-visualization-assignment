import json
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────────────────────────────
# DATASET 1: Hemianopsia  (inline – real patient data from the assignment)
# ─────────────────────────────────────────────────────────────────────
HEMIANOPSIA_DATA = {
    "time": 1709550269540,#the time of the experiment
    "id": "Hemianopsia-396373",#the id of the patient
    "fakePercent": 0,#the percentage of fake data
    "unSeenPoints": [
        {"z": 55.138145446777344, "x": -20.06864356994629, "y": -6.167179107666016}#the unseen points
    ],
    "fixationPercent": 100,#the percentage of fixation
    "reactionTimes": [#the reaction times
        682.70, 391.75, 362.61, 306.42, 291.98, 265.01, 374.38, 343.15,#reaction times in ms
        334.64, 290.01, 321.00, 320.36, 306.85, 347.71, 320.56,#reaction times in ms
        292.50, 583.44, 376.84, 457.56#reaction times in ms
    ],
    "seenPoints": [#the seen points
        {"y": -19.20852279663086,  "z": 54.938087463378906,  "x": -9.687067985534668},#the seen points  
        {"y": -6.167180061340332,  "z": 57.78535842895508,   "x": 10.189117431640625},#the seen points
        {"x": -10.168876647949219, "z": 57.67055892944336,   "y": 7.1902923583984375},#the seen points
        {"x": 10.168876647949219,  "z": 57.67055892944336,   "y": 7.1902923583984375},#the seen points
        {"y": -6.167180061340332,  "z": 57.78535842895508,   "x": -10.189117431640625},#the seen points
        {"y": -6.167180061340332,  "z": 58.67679214477539,   "x": 0},#the seen points
        {"z": 55.02861022949219,   "x": 20.028778076171875,  "y": 7.190291404724121},#the seen points
        {"y": 20.17919158935547,   "z": 54.599578857421875,  "x": -9.627378463745117},#the seen points
        {"z": 55.441864013671875,  "y": 20.179189682006836,  "x": 0},#the seen points
        {"y": 7.190291881561279,   "z": 58.56022262573242,   "x": 0},#the seen points
        {"y": -19.20852279663086,  "x": 9.687067985534668,   "z": 54.938087463378906},#the seen points
        {"z": 52.42131042480469,   "y": -19.20852279663086,  "x": 19.079801559448242},#the seen points
        {"y": 7.190291404724121,   "z": 55.02861022949219,   "x": -20.028778076171875},
        {"y": 20.17919158935547,   "z": 54.599578857421875,  "x": 9.627378463745117},
        {"z": 55.138145446777344,  "y": -6.167179107666016,  "x": 20.06864356994629},
        {"x": -19.079801559448242, "y": -19.20852279663086,  "z": 52.42131042480469},
        {"z": 52.09830856323242,   "y": 20.179189682006836,  "x": 18.96223258972168},
        {"z": 52.09830856323242,   "y": 20.179189682006836,  "x": -18.96223258972168},
        {"x": 0,                   "z": 55.78559494018555,   "y": -19.208520889282227}
    ],
    "settings": {
        "speed": 2, "stimuliCount": 10,#speed of the experiment
        "fakeChance": 0.2, "verticalFOV": 40,#the percentage of fake data
        "delay": 1, "horizontalFOV": 40#horizontal field of view
    }
}

# ─────────────────────────────────────────────────────────────────────
# DATASET 2: Motor Amplification  (load from json files)
# ─────────────────────────────────────────────────────────────────────
def load_motor_data(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load {path}: {e}")
        return None

motor_005774 = load_motor_data("005774.json")
motor_479379 = load_motor_data("479379.json")
motor_926818 = load_motor_data("926818.json")
star_341980  = load_motor_data("341980.json")

# ─────────────────────────────────────────────────────────────────────
# CHART 1: Hemianopsia 3D Scatter
# ─────────────────────────────────────────────────────────────────────
def make_hemianopsia_chart():
    d = HEMIANOPSIA_DATA
    seen       = d["seenPoints"]#the seen points
    unseen     = d["unSeenPoints"]#the unseen points
    rt         = d["reactionTimes"]#the reaction times
    settings   = d["settings"]#the settings
    fix_pct    = d["fixationPercent"]#the percentage of fixation

    fig = go.Figure()

    # Seen points – colored by reaction time (Viridis scale)
    fig.add_trace(go.Scatter3d(
        x=[p["x"] for p in seen],#the x coordinates of the seen points
        y=[p["y"] for p in seen],#the y coordinates of the seen points
        z=[p["z"] for p in seen],#the z coordinates of the seen points
        mode="markers",
        name="Seen points",
        marker=dict(
            size=8,#the size of the markers
            color=rt,#the color of the markers
            colorscale="Viridis",#the color scale of the markers
            colorbar=dict(title="Reaction time (ms)", x=1.05),#the color bar of the markers
            opacity=0.9,  
            line=dict(color="white", width=0.5),#the line of the markers
        ),
        text=[f"Reaction: {r:.1f} ms" for r in rt],#the reaction times
        hovertemplate="<b>Seen</b><br>x=%{x:.2f}  y=%{y:.2f}  z=%{z:.2f}<br>%{text}<extra></extra>",#the hover template
    ))

    # Unseen points – red diamonds
    fig.add_trace(go.Scatter3d(
        x=[p["x"] for p in unseen],#the x coordinates of the unseen points
        y=[p["y"] for p in unseen],#the y coordinates of the unseen poin    ts
        z=[p["z"] for p in unseen],#the z coordinates of the unseen points
        mode="markers",
        name="Unseen points",
        marker=dict(size=10, color="#FF4444", symbol="diamond", opacity=0.95,
                    line=dict(color="white", width=1)),#the line of the markers
        hovertemplate="<b>Unseen</b><br>x=%{x:.2f}  y=%{y:.2f}  z=%{z:.2f}<extra></extra>",#the hover template
    ))

    # Fixation point at origin (0, 0) projected to mean z
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[55],
        mode="markers+text",
        name="Fixation point",
        marker=dict(size=12, color="black", symbol="cross"),
        text=["Fixation (0,0)"],
        textposition="top center",
        hovertemplate="<b>Fixation point</b><extra></extra>",
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Hemianopsia Visual Field</b><br>"#setting the title
                 f"<sup>ID: {d['id']} | Fixation: {fix_pct}% | "#setting the id
                 f"FOV {settings['horizontalFOV']}°H × {settings['verticalFOV']}°V | "#setting the field of view
                 f"Stimuli seen: {len(seen)} | Unseen: {len(unseen)}</sup>",#setting the number of seen and unseen points
            x=0.5
        ),
        scene=dict(
            xaxis=dict(title="Horizontal (x)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),#setting the x-axis
            yaxis=dict(title="Vertical (y)",   backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),#setting the y-axis
            zaxis=dict(title="Depth (z)",       backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            bgcolor="#f8f9fa",#setting the background color
        ),
        legend=dict(x=0, y=1),
        height=720,
        paper_bgcolor="#ffffff",
    )
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 2: Motor Amplification – Horizontal path (one hand)
# ─────────────────────────────────────────────────────────────────────
def extract_coords(coord_list, axis):
    return [pt[axis] for pt in coord_list]

def make_motor_horizontal(data, title_suffix=""):
    if data is None: #if the data is not loaded
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)#if the data is not loaded, return a figure with the text "Data not loaded"

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"}, #colors for the left hand
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}} #colors for the right hand

    hand_key     = "handData"     if "handData"     in data else None#getting the hand data
    adapted_key  = "adaptedHandData" if "adaptedHandData" in data else None#getting the adapted hand data

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))#adding the actual hand data to the sources
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))#adding the adapted hand data to the sources

    for hand_data, label, dashed in sources:#iterating through the sources
        for entry in hand_data:#iterating through the hand data
            hand  = entry.get("hand", "?")#getting the hand
            hcoords = entry.get("horizontalCoordinates", [])#getting the horizontal coordinates
            if not hcoords:#if the horizontal coordinates are not found
                continue#skipping the current iteration
            x_vals = extract_coords(hcoords, "x")#extracting the x coordinates
            c = colors.get(hand, {"actual": "#aaa", "adapted": "#333"})#getting the colors
            col = c["adapted"] if dashed else c["actual"]

            fig.add_trace(go.Scatter(#adding the scatter plot
                x=list(range(len(x_vals))),#the x values
                  y=x_vals,#the y values
                mode="lines",#the mode of the scatter plot
                name=f"{label} – {hand} (x)",#the name of the scatter plot
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),#the line of the scatter plot
                hovertemplate=f"<b>{label} {hand} – x</b><br>step=%{{x}}<br>x=%{{y:.3f}}<extra></extra>",
            ))

    fig.update_layout(
        title=f"<b>Motor Amplification – Horizontal Movement{title_suffix}</b>",
        xaxis_title="Frame",
        yaxis_title="X coordinate (m)",
        height=500,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.2),
    )
    fig.update_xaxes(gridcolor="#dee2e6")
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 3: Motor Amplification – Vertical path
# ─────────────────────────────────────────────────────────────────────
def make_motor_vertical(data, title_suffix=""):
    if data is None:
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)#if the data is not loaded, return a figure with the text "Data not loaded"

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"}, #colors for the left hand
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}} #colors for the right hand

    hand_key    = "handData"        if "handData"        in data else None#getting the hand data
    adapted_key = "adaptedHandData" if "adaptedHandData" in data else None#getting the adapted hand data

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))

    for hand_data, label, dashed in sources:#iterating through the sources
        for entry in hand_data:#iterating through the hand data
            hand    = entry.get("hand", "?")#getting the hand
            vcoords = entry.get("verticalCoordinates", [])#getting the vertical coordinates
            if not vcoords:#if the vertical coordinates are not found
                continue#skipping the current iteration
            y_vals = extract_coords(vcoords, "y")#extracting the y coordinates
            col = colors.get(hand, {}).get("adapted" if dashed else "actual", "#999")#getting the colors

            fig.add_trace(go.Scatter(#adding the scatter plot
                x=list(range(len(y_vals))),
                y=y_vals,#the y values
                mode="lines",#the mode of the scatter plot
                name=f"{label} – {hand} (y)",#the name of the scatter plot
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),#the line of the scatter plot
                hovertemplate=f"<b>{label} {hand} – y</b><br>step=%{{x}}<br>y=%{{y:.3f}}<extra></extra>",#setting the hover template
            ))

    fig.update_layout(
        title=f"<b>Motor Amplification – Vertical Movement{title_suffix}</b>",#setting the title
        xaxis_title="Frame",#setting the x-axis title
        yaxis_title="Y coordinate (m) – height",#setting the y-axis title
        height=500,
        paper_bgcolor="#ffffff",#setting the paper background color
        plot_bgcolor="#f8f9fa",#setting the plot background color
        legend=dict(orientation="h", y=-0.2),#setting the legend
    )
    fig.update_xaxes(gridcolor="#dee2e6")#setting the x-axis grid color
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")#setting the y-axis grid color
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 4: Motor – 2D top-down path overlay (scatter)
# ─────────────────────────────────────────────────────────────────────
def make_motor_topdown(data, title_suffix=""):#function to make the motor topdown chart
    if data is None:#if the data is not loaded
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)#if the data is not loaded, return a figure with the text "Data not loaded"

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"},#colors for the left hand
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}}

    hand_key    = "handData"        if "handData"        in data else None#getting the hand data
    adapted_key = "adaptedHandData" if "adaptedHandData" in data else None#getting the adapted hand data

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))#adding the actual hand data to the sources
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))#adding the adapted hand data to the sources

    for hand_data, label, dashed in sources:#iterating through the sources
        for entry in hand_data:#iterating through the hand data
            hand    = entry.get("hand", "?")#getting the hand
            hcoords = entry.get("horizontalCoordinates", [])#getting the horizontal coordinates
            if not hcoords:#if the horizontal coordinates are not found
                continue#skipping the current iteration
            xs = extract_coords(hcoords, "x")#extracting the x coordinates
            zs = extract_coords(hcoords, "z")#extracting the z coordinates
            col = colors.get(hand, {}).get("adapted" if dashed else "actual", "#999")

            fig.add_trace(go.Scatter(#adding the scatter plot
                x=xs, y=zs,#the x and y coordinates
                mode="lines+markers",#the mode of the scatter plot
                name=f"{label} – {hand}",#the name of the scatter plot
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),#the line of the scatter plot
                marker=dict(size=4),#the marker of the scatter plot
                hovertemplate=f"<b>{label} {hand}</b><br>x=%{{x:.3f}}<br>z=%{{y:.3f}}<extra></extra>",
            ))

    fig.add_shape(type="circle", xref="x", yref="y",#adding the circle
                  x0=-0.02, y0=-0.02, x1=0.02, y1=0.02,#the coordinates of the circle
                  line_color="#2dc653", fillcolor="#2dc653", opacity=0.4)#the color of the circle

    fig.update_layout(
        title=f"<b>Motor Amplification – Top-Down Path (x vs z){title_suffix}</b>",#setting the title
        xaxis_title="X coordinate (horizontal)",#setting the x-axis title
        yaxis_title="Z coordinate (depth)",#setting the y-axis title
        height=520,
        paper_bgcolor="#ffffff",#setting the paper background color
        plot_bgcolor="#f8f9fa",#setting the plot background color
        legend=dict(orientation="h", y=-0.2),#setting the legend
        yaxis=dict(scaleanchor="x", scaleratio=1),#setting the y-axis scale anchor and scale ratio
    )
    fig.update_xaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")#setting the x-axis grid color
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")#setting the y-axis grid color
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 5: Star Cancellation – 3D scatter of all objects
# ─────────────────────────────────────────────────────────────────────
def make_star_cancellation_3d():
    if star_341980 is None:#if the star_341980 is not loaded
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    objects = star_341980.get("objects", [])#getting the objects
    fig = go.Figure()#creating the figure

    groups = {}
    for obj in objects:
        otype = obj["cancellationObjectType"]#getting the object type
        sel   = obj["selected"]#getting the selected status
        key   = (otype, sel)#setting the key
        if key not in groups:
            groups[key] = {"x": [], "y": [], "z": [], "ids": [], "quads": []}#initializing the groups
        c = obj["coordinate"]#getting the coordinate
        groups[key]["x"].append(c["x"])#appending the x coordinate
        groups[key]["y"].append(c["y"])#appending the y coordinate
        groups[key]["z"].append(c["z"])#appending the z coordinate
        groups[key]["ids"].append(obj["id"])#appending the id
        groups[key]["quads"].append(obj["quadrant"])#appending the quadrant

    # Color/symbol mapping
    style = {
        ("SMALL_STAR", True):   {"color": "#2dc653", "symbol": "diamond",    "size": 8,  "name": "Small Star ✓ Selected"},#color, symbol, size, and name for the small star    
        ("SMALL_STAR", False):  {"color": "#FF4444", "symbol": "diamond",    "size": 8,  "name": "Small Star ✗ Missed"},#color, symbol, size, and name for the small star   
        ("BIG_STAR", True):     {"color": "#3A86FF", "symbol": "circle",     "size": 6,  "name": "Big Star ✓ Selected"},#color, symbol, size, and name for the big star   
        ("BIG_STAR", False):    {"color": "#adb5bd", "symbol": "circle",     "size": 6,  "name": "Big Star ✗ (distractor)"},#color, symbol, size, and name for the big star   
        ("WORD", True):         {"color": "#FB5607", "symbol": "square",     "size": 6,  "name": "Word ✓ Selected"},#color, symbol, size, and name for the word   
        ("WORD", False):        {"color": "#dee2e6", "symbol": "square",     "size": 6,  "name": "Word ✗ (distractor)"},#color, symbol, size, and name for the word   
    }

    for key, pts in groups.items():
        s = style.get(key, {"color": "#999", "symbol": "circle", "size": 5, "name": str(key)})#getting the style
        fig.add_trace(go.Scatter3d(
            x=pts["x"], y=pts["y"], z=pts["z"],#the x, y, and z coordinates
            mode="markers",#the mode of the scatter plot
            name=s["name"],#the name of the scatter plot
            marker=dict(size=s["size"], color=s["color"], symbol=s["symbol"],#the marker of the scatter plot
                        opacity=0.85, line=dict(color="white", width=0.5)),#the marker of the scatter plot
            text=[f"{oid} ({q})" for oid, q in zip(pts["ids"], pts["quads"])],#the text of the scatter plot
            hovertemplate="<b>%{text}</b><br>x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>",#the hover template of the scatter plot
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>Star Cancellation Test</b><br>"#setting the title
                 f"<sup>ID: {star_341980.get('id','')} | "#setting the id
                 f"Objects: {len(objects)} | "#setting the number of objects
                 f"Selected: {sum(1 for o in objects if o['selected'])}/{len(objects)}</sup>",#setting the number of selected objects
            x=0.5#setting the x coordinate of the title
        ),
        scene=dict(
            xaxis=dict(title="X", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),#setting the x-axis title
            yaxis=dict(title="Y (height)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),#setting the y-axis title
            zaxis=dict(title="Z (depth)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),#setting the z-axis title
            bgcolor="#f8f9fa",#setting the background color
        ),
        height=700,
        paper_bgcolor="#ffffff",
        legend=dict(x=0, y=1),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 6: Star Cancellation – Quadrant stats bar chart
# ─────────────────────────────────────────────────────────────────────
def make_star_quadrant_bar():#function to make the star quadrant bar chart
    if star_341980 is None:##if the star_341980 is not loaded
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    qstats = star_341980.get("quadrantStats", [])#getting the quadrant stats
    quads  = [q["quadrantType"].replace("_", " ").title() for q in qstats]#getting the quadrant types
    selected = [q["selectedAmountOfObjects"] for q in qstats]#getting the selected amount of objects
    total    = [q["totalAmountOfObjects"] for q in qstats]#getting the total amount of objects
    pcts     = [q["selectedPercentage"] for q in qstats]#getting the selected percentage

    colors_bar = ["#3A86FF", "#8338EC", "#FF006E", "#FB5607"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quads, y=total, name="Total objects",
        marker_color="#dee2e6",
        text=total, textposition="auto",
    ))
    fig.add_trace(go.Bar(
        x=quads, y=selected, name="Selected",
        marker_color=colors_bar,
        text=[f"{s} ({p}%)" for s, p in zip(selected, pcts)],
        textposition="auto",
    ))

    fig.update_layout(
        title="<b>Star Cancellation – Selection per Quadrant</b>",
        xaxis_title="Quadrant",
        yaxis_title="Number of objects",
        barmode="overlay",
        height=450,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor="#dee2e6")
    fig.update_yaxes(gridcolor="#dee2e6")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 7: Star Cancellation – Object type breakdown (pie)
# ─────────────────────────────────────────────────────────────────────
def make_star_type_pie():
    if star_341980 is None:
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    ostats = star_341980.get("objectStats", [])
    labels = []
    values = []
    for s in ostats:
        lbl = s["cancellationObjectType"].replace("_", " ").title()
        d = s.get("direction", "")
        if d and d != "DIRECTION_UNSPECIFIED":
            lbl += f" ({d.title()})"
        labels.append(lbl)
        values.append(s["selectedAmountOfObjects"])

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=["#adb5bd", "#dee2e6", "#2dc653", "#FF006E"]),
        textinfo="label+value+percent",
        hole=0.35,
    ))
    fig.update_layout(
        title="<b>Star Cancellation – Selected Objects by Type</b>",
        height=450,
        paper_bgcolor="#ffffff",
    )
    return fig


# ─────────────────────────────────────────────────────────────────────
# GRADIO APP
# ─────────────────────────────────────────────────────────────────────
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
# 🏥 XRehab Data Visualization
### Lab exercise — Hemianopsia, Motor Amplification & Star Cancellation
---
""")

    with gr.Tab("👁️ Hemianopsia"):
        gr.Markdown("""
**Hemianopsia Visual Field Test**

Each point represents a stimulus shown in the 40°×40° visual field.
- 🟢 **Seen points** — colored by reaction time (ms). Darker = faster.
- 🔴 **Unseen points** — the patient did not react to these stimuli.
- ⬛ **Fixation point** — the center (0,0) where the patient must keep looking.

Rotate the 3D chart with your mouse!
""")
        hemi_plot = gr.Plot(value=make_hemianopsia_chart())

    with gr.Tab("💪 Motor – 005774"):
        gr.Markdown("""
**Motor Amplification — Patient 005774**

This file contains `handData` only (no adapted data).
- **Solid lines** = actual hand movement
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_005774, " (005774)"))
            gr.Plot(value=make_motor_vertical(motor_005774,   " (005774)"))
        gr.Plot(value=make_motor_topdown(motor_005774, " (005774)"))

    with gr.Tab("💪 Motor – 479379"):
        gr.Markdown("""
**Motor Amplification — Patient 479379**

This file contains both `handData` AND `adaptedHandData`.
- **Solid lines** = actual hand position
- **Dashed lines** = adapted / amplified target position

Compare the gap between where the patient moved and where the app wanted them to reach.
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_479379, " (479379)"))
            gr.Plot(value=make_motor_vertical(motor_479379,   " (479379)"))
        gr.Plot(value=make_motor_topdown(motor_479379, " (479379)"))

    with gr.Tab("💪 Motor – 926818"):
        gr.Markdown("""
**Motor Amplification — Patient 926818**

Another patient dataset with `handData`.
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_926818, " (926818)"))
            gr.Plot(value=make_motor_vertical(motor_926818,   " (926818)"))
        gr.Plot(value=make_motor_topdown(motor_926818, " (926818)"))

    with gr.Tab("⭐ Star Cancellation"):
        gr.Markdown("""
**Star Cancellation Test — 341980**

This neuropsychological test checks for visual neglect.
The patient must find and select all **small stars** among distractors (big stars, words).
- 🟢 **Green diamonds** = small stars the patient found
- 🔴 **Red diamonds** = small stars the patient missed
- 🔵 / ⚪ = big stars and words (distractors)
""")
        gr.Plot(value=make_star_cancellation_3d())
        with gr.Row():
            gr.Plot(value=make_star_quadrant_bar())
            gr.Plot(value=make_star_type_pie())

if __name__ == "__main__":
    demo.launch()
