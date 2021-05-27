'''
Generating vapour pressure graphs given Antoine Coefficients

Want the following:

--> Program to ask for coefficients, A,B,C
--> Program to ask for the temperature in degree celcius
--> Compute the vapour pressure (in mmHg, soon to be other pressures/temperatures)

'''
import streamlit as st
from bokeh.plotting import figure, show 
import numpy as np
import pandas as pd
import openpyxl
import base64
import io

'''
# Plotting Vapour Pressures as a Function of Temperature from Antione's Equation

This is a tool that graphs vapour pressure (mmHg) versus temperature (°C) based off [Antoine's Equation.](https://en.wikipedia.org/wiki/Antoine_equation)

Below you will enter the A, B, and C coefficients, as well as the temperature range for the equation to generate the graph.

'''
st.info("As of now, the default values of the A, B, and C values are set to 1 to avoid the error of division by zero.")

#### Calculations ####

temp_lower = st.number_input("Temperature Lower Bound: ")
temp_upper = st.number_input("Temperature Upper Bound: ")


Coeff_A = st.number_input("A Value: ", value=1e0, step=1e-5, format="%.5f")
Coeff_B = st.number_input("B Value: ", value=1e0, step=1e-5, format="%.3f")
Coeff_C = st.number_input("C Value: ", value=1e0, step=1e-5, format="%.3f")

temps_array = [] #array of temperatures in Deg. Celsius

for temp in np.arange(temp_lower,temp_upper+1): #populates array with temperatures between the tao values given.
    temps_array.append(temp)

mmhg_array = [] #array of the pressure values in mmHg for the calculations below

for temp in range(len(temps_array)): #this is in mmHg 
    Value = 10**(Coeff_A-(Coeff_B/(temps_array[temp]+Coeff_C)))
    rounded_mmhg = round(Value, 4) #rounds values to 4 decimal places 
    mmhg_array.append(rounded_mmhg)

#### Unit Conversions ####

atm_array = []
def atm_conversion(mmhg_array):
    for p_atm in mmhg_array:
        atm_value = p_atm / 760
        rounded_atm = round(atm_value, 4)
        atm_array.append(rounded_atm)

bar_array = []
def bar_conversion(mmhg_array):
    for p_bar in mmhg_array:
        bar_value = p_bar * (1.01325/760)
        rounded_bar = round(bar_value, 4)
        bar_array.append(rounded_bar)

kpa_array = []
def kpa_conversion(mmhg_array):
    for p_kpa in mmhg_array:
        kpa_value = p_kpa * (101.325/760)
        rounded_kpa = round(kpa_value, 4)
        kpa_array.append(rounded_kpa)

#### Variables for Bokeh graph axis ####

x_axis_mmhg = temps_array
y_axis_mmhg = mmhg_array

x_axis_atm = temps_array
y_axis_atm = atm_array

x_axis_bar = temps_array
y_axis_bar = bar_array

x_axis_kpa = temps_array
y_axis_kpa = kpa_array

#### Radio buttons ####

options = st.radio(
    'Pressure Units:',
    ('mmHg','atm','Bar','kPa'
))

#### Statements to execute if option is chosen ####

if options == 'mmHg':

    name_graph_mmHg = st.text_input("Name the graph (optional)", value="Vapour Pressure (mmHg) vs Temperature (°C)")

    p_mmhg = figure(title = f"{name_graph_mmHg}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (mmHg)")

    p_mmhg.line(x_axis_mmhg, y_axis_mmhg, legend_label="Vapour Pressure (mmHg)", line_width = 2) 

    try:
        st.bokeh_chart(p_mmhg,use_container_width=False) #Generates graph for viewing
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

    pd_df_mmhg = pd.DataFrame({
        'Temperature (ºC)': x_axis_mmhg,
        'Vapour Pressure (mmHg)': y_axis_mmhg
    })

    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_mmhg)
    
    towrite = io.BytesIO()
    downloaded_file = pd_df_mmhg.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_mmHg.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

if options == 'atm':

    name_graph_atm = st.text_input("Name the graph (optional)", value="Vapour Pressure (atm) vs Temperature (°C)")

    p_atm = figure(title = f"{name_graph_atm}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (atm)")

    p_atm.line(x_axis_atm, y_axis_atm, legend_label="Vapour Pressure (atm)", line_width = 2) 

    atm_conversion(mmhg_array)

    try:
        st.bokeh_chart(p_atm, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_atm = pd.DataFrame({
        'Temperature (ºC)': x_axis_atm,
        'Vapour Pressure (atm)': y_axis_atm
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_atm)

    towrite = io.BytesIO()
    downloaded_file = pd_df_atm.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_atm.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

if options == 'Bar':
    
    name_graph_bar = st.text_input("Name the graph (optional)", value="Vapour Pressure (Bar) vs Temperature (°C)")
    
    p_bar = figure(title = f"{name_graph_bar}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (Bar)")
    
    p_bar.line(x_axis_bar, y_axis_bar, legend_label="Vapour Pressure (Bar)", line_width = 2)
    
    bar_conversion(mmhg_array)
    
    try:
        st.bokeh_chart(p_bar, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_bar = pd.DataFrame({
        'Temperature (ºC)': x_axis_bar,
        'Vapour Pressure (bar)': y_axis_bar
    })
    
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_bar)

    towrite = io.BytesIO()
    downloaded_file = pd_df_bar.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_bar.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

if options == 'kPa':

    name_graph_kPa = st.text_input("Name the graph (optional)", value="Vapour Pressure (kPa) vs Temperature (°C)")

    p_kpa = figure(title = f"{name_graph_kPa}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (kPa)")

    p_kpa.line(x_axis_kpa, y_axis_kpa, legend_label="Vapour Pressure (kPa)", line_width = 2)

    kpa_conversion(mmhg_array)

    try:
        st.bokeh_chart(p_kpa, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_kpa = pd.DataFrame({
        'Temperature (ºC)': x_axis_kpa,
        'Vapour Pressure (kPa)': y_axis_kpa
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_kpa)

    towrite = io.BytesIO()
    downloaded_file = pd_df_kpa.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_kpa.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

'''
The graph was generated using [Bokeh ver. 2.2.2](https://bokeh.org/) as well as [Python 3.8.5.](https://www.python.org/downloads/release/python)

Thank you for viewing! :grinning:
'''

#### Footer ####

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " by ",
        link("https://thomsmd.ca", "Thomas Lee."),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()
