import gradio as gr#importing gradio
import plotly.express as px#importing plotly express
import plotly.graph_objects as go#importing plotly graph objects

df = px.data.gapminder()#loading the gapminder dataset


def demo_fig_01():#function to create a bar plot
    return px.bar(df[df["country"] == "Belgium"], x="year", y="pop", height=400)#creating a bar plot


def demo_fig_02():#function to create a line plot
    return px.line(x=["a", "b", "c"], y=[1, 3, 2])#creating a line plot


def demo_fig_03():#function to create a scatter plot
    return px.scatter(
        df,#loading the dataset
        x="gdpPercap",#setting the x axis
        y="lifeExp",#setting the y axis
        animation_frame="year",#setting the animation frame
        animation_group="country",#setting the animation group
        size="pop",#setting the size
        color="continent",#setting the color
        hover_name="country",#setting the hover name
        log_x=True,#setting the x axis to log scale
        size_max=55,#setting the max size
        range_x=[100, 100000],#setting the range of x axis
        range_y=[25, 90],#setting the range of y axis
    )


def demo_fig_04():#function to create a histogram
    return px.histogram(df, x="lifeExp", nbins=30, titl e="Life Expectancy Histogram")#creating a histogram


def demo_fig_05():#function to create a box plot
    return px.box(df, x="continent", y="lifeExp", title="Life Expectancy Box Plot")#creating a box plot


def demo_fig_06():#function to create a 3d scatter plot
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=df["gdpPercap"],#setting the x axis
                y=df["lifeExp"],#setting the y axis
                z=df["pop"],#setting the z axis
                mode="markers",#setting the mode
                marker=dict(size=5, color=df["continent"].astype("category").cat.codes),#setting the marker
            )
        ]
    )
    fig.update_layout(title="3D GDP, Life Expectancy, Population", height=800)#setting the layout
    return fig


def demo_fig_07():#function to create a choropleth map
    return px.choropleth(
        df[df["year"] == 2007],#filtering the data
        locations="iso_alpha",#setting the locations
        color="lifeExp",#setting the color
        hover_name="country",#setting the hover name
        title="Life Expectancy by Country (2007)",#setting the title
        color_continuous_scale=px.colors.sequential.Plasma,#setting the color scale
    )


def demo_fig_08():#function to create a figure with multiple traces
    fig = go.Figure()#creating a figure
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines", name="Line Trace"))#adding a line trace
    fig.add_trace(go.Bar(x=[1, 2, 3], y=[7, 8, 9], name="Bar Trace"))#adding a bar trace
    return fig#returning the figure


CHARTS = {
    "Bar Plot": demo_fig_01,#dictionary of charts
    "Line Plot": demo_fig_02,#dictionary of charts
    "Scatter Plot": demo_fig_03,#dictionary of charts
    "Histogram": demo_fig_04,#dictionary of charts
    "Box Plot": demo_fig_05,#dictionary of charts
    "3D Scatter Plot": demo_fig_06,#dictionary of charts
    "Choropleth Map": demo_fig_07,#dictionary of charts
    "Multiple Traces": demo_fig_08,
}


def update_plot(chart_name):
    return CHARTS[chart_name]()


with gr.Blocks() as app:
    gr.Markdown("# 📊 Gapminder Dashboard")
    tabs = gr.Radio(
        choices=list(CHARTS.keys()),#dictionary of charts
        value="Bar Plot",#default value
        label="Select Chart",#label of the tabs
        interactive=True,#interactive tabs
    )
    plot = gr.Plot(value=demo_fig_01())#default plot

    tabs.change(fn=update_plot, inputs=tabs, outputs=plot)#changing the plot when the tabs are changed

app.launch()#launching the app