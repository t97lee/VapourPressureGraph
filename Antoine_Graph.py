'''
Generating vapour pressure graphs given Antoine Coefficients

Want the following:

--> Program to ask for coefficients, A,B,C
--> Program to ask for the temperature in degree celcius
--> Compute the vapour pressure (in mmHg, soon to be other pressures/temperatures)

'''
import streamlit as st
from bokeh.plotting import figure, show 
#from bokeh.io import curdoc --> used to configure the theme of the Bokeh graph but appears to not be working. 
import numpy as np
import pandas as pd
import openpyxl
import base64
import io

'''
# Plotting Vapour Pressures as a Function of Temperature from Antione's Equation

This is a tool that graphs vapour pressure (mmHg) versus temperature (°C) based off [Antoine's Equation](https://en.wikipedia.org/wiki/Antoine_equation)

Below you will enter the A, B, and C coefficients, as well as the temperature range for the equation to generate the graph.

'''
st.info("As of now, the default values of the A, B, and C values are set to 1 to avoid the error of division by zero.")

#### Calculations ####
temps_array = [] #array of temperatures in Deg. Celsius

temp_lower = st.number_input("Temperature Lower Bound: ")
temp_upper = st.number_input("Temperature Upper Bound: ")

for temp in np.arange(temp_lower,temp_upper+1): #populates array with temperatures between the tao values given.
    temps_array.append(temp)

Coeff_A = st.number_input("A Value: ", value=1e0, step=1e-5, format="%.5f")
Coeff_B = st.number_input("B Value: ", value=1e0, step=1e-5, format="%.3f")
Coeff_C = st.number_input("C Value: ", value=1e0, step=1e-5, format="%.3f")

exp_array = [] #array of the pressure values in mmHg for the calculations below

for temp in range(len(temps_array)):
    Value = 10**(Coeff_A-(Coeff_B/(temps_array[temp]+Coeff_C)))
    Rounded_Value = round(Value, 4) #rounds values to 4 decimal places 
    exp_array.append(Rounded_Value)

#### Bokeh configuration ####

x_axis = temps_array
y_axis = exp_array

p = figure(title="Vapour Pressure vs Temperature",
    x_axis_label = "Temperature (°C)",
    y_axis_label = "Vapour Pressure (mmHg)")

p.line(x_axis, y_axis, legend_label="Vapour Pressure", line_width = 2)

#### Error Handling ####
try:
    st.bokeh_chart(p,use_container_width=False) #Generates graph for viewing
except ValueError:
    st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

#### Generate a Table of Values ####

pd_df = pd.DataFrame({
        'Temperature (ºC)': x_axis,
        'Vapour Pressure (mmHg)': y_axis
    })

if st.button('Generate Table of Values', help="Click to generate a table of values"):
    st.write(pd_df)

towrite = io.BytesIO()
downloaded_file = pd_df.to_excel(towrite, encoding='utf-8', index=False, header=True)
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode() 
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Vapour_Pressure_Data.xlsx">Download Excel (.xlsx) File</a>'
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
