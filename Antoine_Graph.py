'''
Generating vapour pressures given Antoine Coefficients

Want the following:

--> Program to ask for coefficients, A,B,C
--> Program to ask for the temperature in degree celcius
--> Compute the vapour pressure (in mmHg)

'''
import streamlit as st
from bokeh.plotting import figure, show
from bokeh.io import curdoc
import numpy as np
import pandas as pd


'''
# Plotting Vapour Pressures as a Function of Temperature from Antione's Equation

This is a tool that graphs vapour pressure (mmHg) versus temperature (°C) based off [Antoine's Equation](https://en.wikipedia.org/wiki/Antoine_equation)

Below you will enter the A, B, and C coefficients, as well as the temperature range for the equation to generate the graph.

'''
st.info("As of now, the default values of the A, B, and C values are set to 1 to avoid the error of division by zero.")

ex = RuntimeWarning("This error is showing due to out of range values most likely caused by the lack of an appropriate C value but if the graph is present, you should be okay. "
"I am currently trying to find a fix for this.")

st.exception(ex) #raise an exception for a RuntimeWarning 

#### Calculations ####
temps_array = [] #array of temperatures in Deg. Celsius

temp_lower = st.number_input("Temperature Lower Bound: ")
temp_upper = st.number_input("Temperature Upper Bound: ")

for temp in np.arange(temp_lower,temp_upper+1): #adds the temperature between each element
    temps_array.append(temp)

Coeff_A = st.number_input("A Value: ", value=1e0, step=1e-5, format="%.5f")
Coeff_B = st.number_input("B Value: ", value=1e0, step=1e-5, format="%.3f")
Coeff_C = st.number_input("C Value: ", value=1e0, step=1e-5, format="%.3f")

exp_array = [] #array of the pressure values in mmHg for the calculations below

try:
    for temp in range(len(temps_array)):
        Value = 10**(Coeff_A-(Coeff_B/(temps_array[temp]+Coeff_C)))
        Rounded_Value = round(Value, 3)
        exp_array.append(Rounded_Value)
except ValueError:
    st.markdown("You may not divide by zero")

#### Bokeh configuration ####

x_axis = temps_array
y_axis = exp_array

p = figure(title="Vapour Pressure vs Temperature",
    x_axis_label = "Temperature (°C)",
    y_axis_label = "Vapour Pressure (mmHg)")

p.line(x_axis, y_axis, legend_label="Vapour Pressure", line_width = 2)

st.bokeh_chart(p,use_container_width=False)

#### Generate a Table of Values ####
if st.button('Generate Table of Values', help="Click to generate a table of values"):
    st.write(pd.DataFrame({
        'Temperature (ºC)': x_axis,
        'Vapour Pressure (mmHg)': y_axis
    }))


'''
The graph was generated using [Bokeh ver. 2.2.2](https://bokeh.org/) as well as [Python 3.8.5](https://www.python.org/downloads/release/python)

Additionally, I currently have a list of things to add to this once I find out how to incorporate them:

* Output graphs for various units of pressure and temperature other than mmHg (e.g. atm, kPa, Pa, °F, K, etc)

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
