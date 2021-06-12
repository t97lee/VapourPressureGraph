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

st.set_page_config(
    page_title = "Vapour Pressure Graph Generator",
    page_icon = "random",
    layout = "centered"
)

'''
# Plotting Vapour Pressures as a Function of Temperature from Antione's Equation

This is a tool that graphs vapour pressure versus temperature based off [Antoine's Equation.](https://en.wikipedia.org/wiki/Antoine_equation)

Below you will enter the A, B, and C coefficients, as well as the temperature range for the equation to generate the graph. The options to convert the 
units of pressure and temperature are provided towards the bottom. 

'''
st.info("As of now, the default values of the A, B, and C values are set to 1 to avoid the error of division by zero.")
st.info("Additionally, the calculator currently only takes °C as units for temperature inputs which can be converted via the options below. ")


temp_lower = st.number_input("Temperature Lower Bound (°C): ")
temp_upper = st.number_input("Temperature Upper Bound (°C): ")

Coeff_A = st.number_input("A Value: ", value=1e0, step=1e-5, format="%.5f")
Coeff_B = st.number_input("B Value: ", value=1e0, step=1e-5, format="%.3f")
Coeff_C = st.number_input("C Value: ", value=1e0, step=1e-5, format="%.3f")

#### Radio buttons ####

options_pressure = st.radio(
    'Pressure Units:',
    ('mmHg','atm','Bar','kPa'))

options_temperature = st.radio(
    'Temperature Units:',
    ('°C','K','°F'))

temps_array = [temp_a for temp_a in np.arange(temp_lower, temp_upper +1)] #array of temperatures in deg. celsius

#### Calculations ####

mmhg_array = [] #initialize empty list
for temp in range(len(temps_array)): 
    Value = 10**(Coeff_A-(Coeff_B/(temps_array[temp]+Coeff_C))) #Computes the vapour pressure in mmHg and °C
    rounded_mmhg = round(Value, 4) #rounds values to 4 decimal places 
    mmhg_array.append(rounded_mmhg)

mmhg_array = [temp for temp in range(len(temps_array))]

#### unit conversions and classes ####

class pressures:
    def __init__ (self, pressure_input):
        self.pressure = pressure_input
    
    def mmhg(self):
        return self.pressure
    
    def atm(self):
        atm_array = [(pressure / 760) for pressure in self.pressure]
        return atm_array

    def bar(self):
        bar_array = [(pressure * (1.01325/760)) for pressure in self.pressure]
        return bar_array
    
    def kpa(self):
        kpa_array = [(pressure * (101.325/760)) for pressure in self.pressure]
        return kpa_array

pressure = pressures(mmhg_array)

class temperature:
    def __init__ (self, temp_input):
        self.temp_input = temp_input
    
    def celcius(self):
        return self.temp_input
    
    def kelvin(self):
        kelvin = [temps + 273.15 for temps in self.temp_input]
        return kelvin
    
    def fahrenheit(self):
        fahrenheit = [((temps*9/5) + 32) for temps in self.temp_input]
        return fahrenheit

temps = temperature(temps_array)

#### Functions for determining the graphs ####

def mmhg_celcius():

    x_axis_mmhg = temps.celcius()
    y_axis_mmhg = pressure.mmhg()

    name_graph_mmHg = st.text_input("Name the graph (optional)", value="Vapour Pressure (mmHg) vs Temperature (°C)")

    p_mmhg_c = figure(title = f"{name_graph_mmHg}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (mmHg)")

    p_mmhg_c.line(x_axis_mmhg, y_axis_mmhg, legend_label="Vapour Pressure (mmHg)", line_width = 2) 

    try:
        st.bokeh_chart(p_mmhg_c,use_container_width=False) #Generates graph for viewing
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

    pd_df_mmhg_c = pd.DataFrame({
        'Temperature (ºC)': x_axis_mmhg,
        'Vapour Pressure (mmHg)': y_axis_mmhg
    })

    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_mmhg_c)

    towrite = io.BytesIO()
    downloaded_file = pd_df_mmhg_c.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_mmHg.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def mmhg_kelvin():

    x_axis_mmhg_k = temps.kelvin()
    y_axis_mmhg_k = pressure.mmhg()

    name_graph_mmhg_k = st.text_input("Name the graph (optional)", value="Vapour Pressure (mmHg) vs Temperature (K)")

    p_mmhg_k = figure(title = f"{name_graph_mmhg_k}",
        x_axis_label = "Temperature (K)",
        y_axis_label = "Vapour Pressure (mmHg)")

    p_mmhg_k.line(x_axis_mmhg_k, y_axis_mmhg_k, legend_label="Vapour Pressure (mmHg)", line_width = 2) 

    try:
        st.bokeh_chart(p_mmhg_k,use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

    pd_df_mmhg_k = pd.DataFrame({
        'Temperature (K)': x_axis_mmhg_k,
        'Vapour Pressure (mmHg)': y_axis_mmhg_k
    })

    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_mmhg_k)

    towrite = io.BytesIO()
    downloaded_file = pd_df_mmhg_k.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)   
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_mmHg.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def mmhg_f():

    x_axis_mmhg_f = temps.fahrenheit()
    y_axis_mmhg_f = pressure.mmhg()

    name_graph_mmhg_f = st.text_input("Name the graph (optional)", value="Vapour Pressure (mmHg) vs Temperature (°F)")

    p_mmhg_f = figure(title = f"{name_graph_mmhg_f}",
        x_axis_label = "Temperature (°F)",
        y_axis_label = "Vapour Pressure (mmHg)")

    p_mmhg_f.line(x_axis_mmhg_f, y_axis_mmhg_f, legend_label="Vapour Pressure (mmHg)", line_width = 2) 

    try:
        st.bokeh_chart(p_mmhg_f,use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

    pd_df_mmhg_f = pd.DataFrame({
        'Temperature (ºF)': x_axis_mmhg_f,
        'Vapour Pressure (mmHg)': y_axis_mmhg_f
    })

    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_mmhg_f)

    towrite = io.BytesIO()
    downloaded_file = pd_df_mmhg_f.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_mmHg.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def atm_c():

    x_axis_atm_c = temps.celcius()
    y_axis_atm_c = pressure.atm()

    name_graph_atm_c = st.text_input("Name the graph (optional)", value="Vapour Pressure (atm) vs Temperature (°C)")

    p_atm_c = figure(title = f"{name_graph_atm_c}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (atm)")

    p_atm_c.line(x_axis_atm_c, y_axis_atm_c, legend_label="Vapour Pressure (atm)", line_width = 2) 

    try:
        st.bokeh_chart(p_atm_c, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")

    pd_df_atm_c = pd.DataFrame({
        'Temperature (ºC)': x_axis_atm_c,
        'Vapour Pressure (atm)': y_axis_atm_c
    })

    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_atm_c)

    towrite = io.BytesIO()
    downloaded_file = pd_df_atm_c.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_atm.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def atm_k():

    x_axis_atm_k = temps.kelvin()
    y_axis_atm_k = pressure.atm()
    
    name_graph_atm_k = st.text_input("Name the graph (optional)", value="Vapour Pressure (atm) vs Temperature (K)")

    p_atm_k = figure(title = f"{name_graph_atm_k}",
        x_axis_label = "Temperature (K)",
        y_axis_label = "Vapour Pressure (atm)")

    p_atm_k.line(x_axis_atm_k, y_axis_atm_k, legend_label="Vapour Pressure (atm)", line_width = 2) 

    pressure.atm()

    try:
        st.bokeh_chart(p_atm_k, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_atm_k = pd.DataFrame({
        'Temperature (K)': x_axis_atm_k,
        'Vapour Pressure (atm)': y_axis_atm_k
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_atm_k)

    towrite = io.BytesIO()
    downloaded_file = pd_df_atm_k.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_atm.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def atm_f():

    x_axis_atm_f = temps.fahrenheit()
    y_axis_atm_f = pressure.atm()

    name_graph_atm_f = st.text_input("Name the graph (optional)", value="Vapour Pressure (atm) vs Temperature (°F)")

    p_atm_f = figure(title = f"{name_graph_atm_f}",
        x_axis_label = "Temperature (°F)",
        y_axis_label = "Vapour Pressure (atm)")

    p_atm_f.line(x_axis_atm_f, y_axis_atm_f, legend_label="Vapour Pressure (atm)", line_width = 2) 

    pressure.atm()

    try:
        st.bokeh_chart(p_atm_f, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_atm_f = pd.DataFrame({
        'Temperature (ºF)': x_axis_atm_f,
        'Vapour Pressure (atm)': y_axis_atm_f
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_atm_f)

    towrite = io.BytesIO()
    downloaded_file = pd_df_atm_f.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_atm.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)


def bar_c():

    x_axis_bar_c = temps.celcius()
    y_axis_bar_c = pressure.bar()

    name_graph_bar_c = st.text_input("Name the graph (optional)", value="Vapour Pressure (Bar) vs Temperature (°C)")
    
    p_bar = figure(title = f"{name_graph_bar_c}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (Bar)")
    
    p_bar.line(x_axis_bar_c, y_axis_bar_c, legend_label="Vapour Pressure (Bar)", line_width = 2)
    
    pressure.bar()
    
    try:
        st.bokeh_chart(p_bar, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_bar_c = pd.DataFrame({
        'Temperature (ºC)': x_axis_bar_c,
        'Vapour Pressure (Bar)': y_axis_bar_c
    })
    
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_bar_c)

    towrite = io.BytesIO()
    downloaded_file = pd_df_bar_c.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_bar.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def bar_k():

    x_axis_bar_k = temps.kelvin()
    y_axis_bar_k = pressure.bar()

    name_graph_bar_k = st.text_input("Name the graph (optional)", value="Vapour Pressure (Bar) vs Temperature (K)")
    
    p_bar_k = figure(title = f"{name_graph_bar_k}",
        x_axis_label = "Temperature (K)",
        y_axis_label = "Vapour Pressure (Bar)")
    
    p_bar_k.line(x_axis_bar_k, y_axis_bar_k, legend_label="Vapour Pressure (Bar)", line_width = 2)
    
    pressure.bar()
    
    try:
        st.bokeh_chart(p_bar_k, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_bar_k = pd.DataFrame({
        'Temperature (K)': x_axis_bar_k,
        'Vapour Pressure (Bar)': y_axis_bar_k
    })
    
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_bar_k)

    towrite = io.BytesIO()
    downloaded_file = pd_df_bar_k.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_bar.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def bar_f():

    x_axis_bar_f = temps.fahrenheit()
    y_axis_bar_f = pressure.bar()

    name_graph_bar_f = st.text_input("Name the graph (optional)", value="Vapour Pressure (Bar) vs Temperature (°F)")
    
    p_bar_f = figure(title = f"{name_graph_bar_f}",
        x_axis_label = "Temperature (°F)",
        y_axis_label = "Vapour Pressure (Bar)")
    
    p_bar_f.line(x_axis_bar_f, y_axis_bar_f, legend_label="Vapour Pressure (Bar)", line_width = 2)
    
    pressure.bar()
    
    try:
        st.bokeh_chart(p_bar_f, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_bar_f = pd.DataFrame({
        'Temperature (°F)': x_axis_bar_f,
        'Vapour Pressure (Bar)': y_axis_bar_f
    })
    
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_bar_f)

    towrite = io.BytesIO()
    downloaded_file = pd_df_bar_f.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_bar.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def kpa_c():
    
    x_axis_kpa = temps.celcius()
    y_axis_kpa = pressure.kpa()

    name_graph_kPa_c = st.text_input("Name the graph (optional)", value="Vapour Pressure (kPa) vs Temperature (°C)")

    p_kpa_c = figure(title = f"{name_graph_kPa_c}",
        x_axis_label = "Temperature (°C)",
        y_axis_label = "Vapour Pressure (kPa)")

    p_kpa_c.line(x_axis_kpa, y_axis_kpa, legend_label="Vapour Pressure (kPa)", line_width = 2)

    pressure.kpa()

    try:
        st.bokeh_chart(p_kpa_c, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_kpa_c = pd.DataFrame({
        'Temperature (ºC)': x_axis_kpa,
        'Vapour Pressure (kPa)': y_axis_kpa
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_kpa_c)

    towrite = io.BytesIO()
    downloaded_file = pd_df_kpa_c.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_kpa.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def kpa_k():

    x_axis_kpa_k = temps.kelvin()
    y_axis_kpa_k = pressure.kpa()

    name_graph_kPa_k = st.text_input("Name the graph (optional)", value="Vapour Pressure (kPa) vs Temperature (K)")

    p_kpa_k = figure(title = f"{name_graph_kPa_k}",
        x_axis_label = "Temperature (K)",
        y_axis_label = "Vapour Pressure (kPa)")

    p_kpa_k.line(x_axis_kpa_k, y_axis_kpa_k, legend_label="Vapour Pressure (kPa)", line_width = 2)

    pressure.kpa()

    try:
        st.bokeh_chart(p_kpa_k, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_kpa_k = pd.DataFrame({
        'Temperature (K)': x_axis_kpa_k,
        'Vapour Pressure (kPa)': y_axis_kpa_k
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_kpa_k)

    towrite = io.BytesIO()
    downloaded_file = pd_df_kpa_k.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_kpa.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

def kpa_f():

    x_axis_kpa_f = temps.fahrenheit()
    y_axis_kpa_f = pressure.kpa()

    name_graph_kPa_f = st.text_input("Name the graph (optional)", value="Vapour Pressure (kPa) vs Temperature (°F)")

    p_kpa_f = figure(title = f"{name_graph_kPa_f}",
        x_axis_label = "Temperature (°F)",
        y_axis_label = "Vapour Pressure (kPa)")

    p_kpa_f.line(x_axis_kpa_f, y_axis_kpa_f, legend_label="Vapour Pressure (kPa)", line_width = 2)

    pressure.kpa()

    try:
        st.bokeh_chart(p_kpa_f, use_container_width=False)
    except ValueError:
        st.error("Your values are out of range for Bokeh to display a graph, try to input smaller values (in particular for your C value) or make a pull request/issue on Github. Thank you!")
        
    pd_df_kpa_f = pd.DataFrame({
        'Temperature (°F)': x_axis_kpa_f,
        'Vapour Pressure (kPa)': y_axis_kpa_f
    })
    if st.button('Generate Table of Values', help="Click to generate a table of values"):
        st.write(pd_df_kpa_f)

    towrite = io.BytesIO()
    downloaded_file = pd_df_kpa_f.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)  
    b64 = base64.b64encode(towrite.read()).decode() 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="PVap_kpa.xlsx">Download Excel (.xlsx) File</a>'
    st.markdown(linko, unsafe_allow_html=True)

#### Statements to execute if option is chosen ####

if options_pressure == 'mmHg' and options_temperature == '°C':
    mmhg_celcius()

if options_pressure == 'mmHg' and options_temperature == 'K':
    mmhg_kelvin()

if options_pressure == 'mmHg' and options_temperature == '°F':
    mmhg_f()

if options_pressure == 'atm' and options_temperature == '°C':
    atm_c()

if options_pressure == 'atm' and options_temperature == "K":
    atm_k()

if options_pressure == 'atm' and options_temperature == "°F":
    atm_f()

if options_pressure == 'Bar' and options_temperature == '°C':
    bar_c()

if options_pressure == 'Bar' and options_temperature == 'K':
    bar_k()

if options_pressure == 'Bar' and options_temperature == '°F':
    bar_f() 

if options_pressure == 'kPa' and options_temperature == '°C':
    kpa_c()

if options_pressure == 'kPa' and options_temperature == 'K':
    kpa_k()

if options_pressure == 'kPa' and options_temperature == '°F':
    kpa_f()

'''
The graph was generated using [Bokeh ver. 2.2.2](https://bokeh.org/) as well as [Python 3.8.5.](https://www.python.org/downloads/release/python)

Thank you for viewing! :grinning: 

Created by [Thomas Lee](https://thomsmd.ca). View on Github [here.](https://github.com/thomaslee01/VapourPressureGraph)
'''
