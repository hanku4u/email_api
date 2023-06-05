#write a function that will data a dataframe and create a seaborn grouped bar chart. The chart should have a line chart at the top as well
# the function should save the chart as a base64 string and return it
def grouped_bar_chart(df, x, y, hue, title, xlabel, ylabel, legend_title, legend_labels, line_x, line_y, line_label):
    # create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # create the bar chart
    sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax)
    
    # create the line chart
    sns.lineplot(x=line_x, y=line_y, data=df, ax=ax, color='black', label=line_label)
    
    # set the title
    ax.set_title(title)
    
    # set the x and y labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # set the legend title and labels
    ax.legend(title=legend_title, labels=legend_labels)
    
    # save the figure as a base64 string
    figdata = utils.fig_to_base64(fig)
    
    # return the base64 string
    return figdata


# write the fig_to_base64 function
def fig_to_base64(fig):
    # save the figure to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    
    # encode the buffer to base64
    figdata = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    # close the buffer
    buf.close()
    
    # return the base64 string
    return figdata