import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Div, BoxZoomTool, ResetTool
from bokeh.embed import file_html


def bokeh_scatter(df):

        output_file("book_map.html", title="Book Map")

        desc = Div(text=open("description.html", 'r').read(), width=800)

        source = ColumnDataSource(data=dict(x=[], y=[], 
                title=[], author=[]))

        source.data = dict(
                x = df['X'],
                y = df['Y'],
                author = df['Author'],
                title = df['Title'],
        )

        hover = HoverTool(tooltips=[
                ("Author", "@author"),
		("Title", "@title")
        ])

        p = figure(plot_width=1200, plot_height=800,
           title='Project Gutenberg Book Map', toolbar_location="below", 
           tools=[hover, BoxZoomTool(),ResetTool()])


        p.circle(x='x', y='y', size=7, 
                source=source, line_color=None)

        
        show(p)
