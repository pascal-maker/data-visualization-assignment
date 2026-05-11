import json
import gradio as gr
import plotly.graph_objects as go

try:
    with open("hemianopsia.json", "r") as f: #loading the json file
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):   #if the json file is not found or empty
    print("Warning: hemianopsia.json not found or empty. Using dummy data!")
    data = {
        "seenPoints": [{"x": 10, "y": 10, "z": 50}, {"x": -20, "y": 5, "z": 45}],
        "unSeenPoints": [{"x": 30, "y": -10, "z": 40}, {"x": 15, "y": 20, "z": 55}],
        "reactionTimes": [250.5, 320.1]
    }

def make_hemianopsia_chart(): #function to make the hemianopsia chart
    seen = data.get("seenPoints", [])#getting the seen points
    unseen = data.get("unSeenPoints", [])#getting the unseen points
    reaction_times = data.get("reactionTimes", [])

    fig = go.Figure()

    # seen points
    if seen:
        fig.add_trace(
            go.Scatter3d(
                x=[p["x"] for p in seen],#setting the x coordinates of the seen points
                y=[p["y"] for p in seen],#setting the y coordinates of the seen points
                z=[p["z"] for p in seen],#setting the z coordinates of the seen points
                mode="markers",
                name="Seen points",#setting the name of the seen points
                marker=dict(
                    size=6,
                    color=reaction_times,#setting the color of the seen points
                    colorscale="Viridis",
                    colorbar=dict(title="Reaction time (ms)"),#setting the color bar title
                ),
                text=[f"Reaction: {rt:.1f} ms" for rt in reaction_times],
                hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<br>%{text}<extra></extra>",#setting the hover template
            )
        )

    # unseen points
    if unseen:#if there are unseen points
        fig.add_trace(#adding the unseen points
            go.Scatter3d(
                x=[p["x"] for p in unseen],#setting the x coordinates of the unseen points
                y=[p["y"] for p in unseen],#setting the y coordinates of the unseen points
                z=[p["z"] for p in unseen],#setting the z coordinates of the unseen points
                mode="markers",#setting the mode of the unseen points
                name="Unseen points",#setting the name of the unseen points
                marker=dict(size=8, color="red", symbol="diamond"),#setting the marker of the unseen points
                hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<br>Unseen<extra></extra>",#setting the hover template
            )
        )

    # fixation center
    fig.add_trace(#adding the fixation center
        go.Scatter3d(
            x=[0],#setting the x coordinates of the fixation center
            y=[0],#setting the y coordinates of the fixation center
            z=[55],#setting the z coordinates of the fixation center
            mode="markers+text",
            name="Fixation point",#setting the name of the fixation point
            marker=dict(size=10, color="black"),#setting the marker of the fixation point
            text=["Fixation"],#setting the text of the fixation point
            textposition="top center",#setting the text position of the fixation point
        )
    )

    fig.update_layout(#updating the layout
        title="Hemianopsia Visual Field",#setting the title
        scene=dict(
            xaxis_title="Horizontal",#setting the x-axis title
            yaxis_title="Vertical",#setting the y-axis title
            zaxis_title="Depth",#setting the z-axis title
        ),
        height=700,
    )
    return fig

with gr.Blocks() as demo:#creating the demo
    gr.Markdown("# Hemianopsia Visualization")  #setting the title
    gr.Markdown("This 3D chart maps seen vs unseen points in the visual field, including reaction times.")#setting the description
    plot = gr.Plot(value=make_hemianopsia_chart())#creating the plot

if __name__ == "__main__":
    demo.launch()#launching the demo
