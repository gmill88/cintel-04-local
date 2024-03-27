import plotly.express as px
from shiny.express import input, ui
from shiny import render, reactive
from shinywidgets import render_plotly
import pandas as pd
import seaborn as sns
from palmerpenguins import load_penguins

# load penguins dataset
penguins_df = load_penguins()

ui.page_opts(title="Miller Penguin Data")

# add ui sidebar
with ui.sidebar(open="open"):
    ui.h2("Sidebar") # add second level header to sidebar
    
    # Dropdown to select attribute 
    ui.input_selectize("selected_attribute", "Body Measurement in Millimeters", 
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]) 
    
    # input for number of bins
    ui.input_numeric("plotly_bin_count", "Bin Count", 25)
    
    # create slider
    ui.input_slider("seaborn_bin_count", "Bin Count", 3, 100, 25)

    # Create a checkbox group input to filter the species
    ui.input_checkbox_group("species_list", "Selected species", 
                            ["Adelie", "Chinstrap", "Gentoo"], selected=["Adelie", "Chinstrap"], inline=True)

        # Create a checkbox group input to filter the island
    ui.input_checkbox_group("island_list", "Selected island", 
                            ["Torgersen", "Biscoe", "Dream"], selected=["Torgersen", "Biscoe", "Dream"], inline=True)
    
    # Add a horizontal rule to the sidebar
    ui.hr()

    # Add a hyperlink to the sidebar
    ui.a("Miller Repo", href="https://github.com/gmill88/cintel-03-reactive", target="_blank")
    
    # display data grid and data table
with ui.layout_columns():        
    with ui.card(full_screen=True):
        ui.card_header("Penguins Data Table")
        @render.data_frame
        def render_penguins_table():
            return filtered_data()
        
with ui.layout_columns(): 
    with ui.card(full_screen=True):
        ui.card_header("Penguins Data Grid")
        @render.data_frame
        def penguins_data():
            return render.DataGrid(data=filtered_data(), row_selection_mode="multiple") 

# Plotly histogram showing all species
with ui.card(full_screen=True):
    ui.card_header("Plotly Histogram")
    @render_plotly  
    def plot_plt():  
        return px.histogram(filtered_data(),
            x=input.selected_attribute(),
            nbins=input.plotly_bin_count(),
            color="species",
            title="Penguin bill depth",
            labels={"selected_attribute": "Selected Attribute", "count": "Count"})
        
# Seaborn histogram showing all species
with ui.card(full_screen=True):
    ui.card_header("Seaborn Histogram")

    @render.plot(alt="Seaborn Histogram")
    def seaborn_histogram():
        histplot = sns.histplot(filtered_data(), x=input.selected_attribute(), bins=input.seaborn_bin_count())
        histplot.set_title("Penguin Data")
        histplot.set_xlabel("Selected Attribute")
        histplot.set_ylabel("Count")
        return histplot
        
# Plotly Scatterplot showing all species
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(filtered_data(),
            x="bill_depth_mm",
            y="flipper_length_mm",
            color="species",
            hover_name="island",
            title="Scatterplot of Bill Length vs. Body Mass by Species",
            labels={
                "bill_depth_mm": "Bill Depth (mm)",
                "flipper_length_mm": "Flipper Length (mm)"})
        
# 3d scatterplot showing all species
with ui.card(full_screen=True):
    ui.card_header("3D Scatter Plot Penguin Data")

    @render_plotly
    def scatter_3d_plot():
        return px.scatter_3d(
            filtered_data(),
            x="body_mass_g",
            y="bill_depth_mm",
            z="flipper_length_mm",
            color="species",
            hover_name="island",
            title="3D Scatter Plot of Body Mass, Bill Length, and Flipper Length",
            labels={
                "body_mass_g": "Body Mass (g)",
                "bill_depth_mm": "Bill Depth (mm)",
                "flipper_length_mm": "Flipper Length (mm)"})


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.species_list()) & penguins_df["island"].isin(input.island_list())]
