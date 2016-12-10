import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Div, BoxZoomTool, ResetTool, Title
from bokeh.embed import file_html
from bokeh.palettes import Accent6 as palette

def make_caption(df):

	n_rows = [len(df[df.Cluster == i].Author) for i in set(df.Cluster)]
	max_row = max(n_rows)

	cols_rows = []
	for i in set(df.Cluster):
		cols = []
		for index, row in df[df.Cluster == i].iterrows():
			cols.append(row.Title + ' - ' + row.Author)

		cols_rows.append(cols) 

	char_len = max([len(j) for i in cols_rows for j in i])

	for i, col in enumerate(cols_rows):
		if len(col) < max_row:
			cols_rows[i] = cols_rows[i] + ['']*(max_row - len(col))	

	out_string = ''
	for j in range(len(cols_rows[0])):
		line = ''
		for i in range(len(cols_rows)):
			book = cols_rows[i][j]
			
			if len(book) < char_len:
				book += ' '*(char_len - len(book))
				
			book += '\t'
			line += book

		out_string += line + '\n'
			
	
	return out_string


def bokeh_scatter(df):

	output_file("book_map.html", title="Book Map")

	desc = Div(text=open("description.html", 'r').read(), width=1000)

	source = ColumnDataSource(data=dict(x=[], y=[], 
		title=[], author=[], colour=[]))

	color_map = lambda x: palette[x]
	df['Colour'] = df.Cluster.apply(color_map)


	source.data = dict(
		x = df['X'],
		y = df['Y'],
		author = df['Author'],
		title = df['Title'],
		colour = df['Colour']
	)

	hover = HoverTool(tooltips=[
		("Author", "@author"),
		("Title", "@title")
	])

	p = figure(plot_width=1000, plot_height=700,
		title='Project Gutenberg Book Map', toolbar_location="below", 
		tools=[hover, BoxZoomTool(),ResetTool()])


	p.circle(x='x', y='y', size=7, color='colour',
		source=source, line_color=None)
 
	show(p)
