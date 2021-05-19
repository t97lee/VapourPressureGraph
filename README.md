# Graphing Vapour Pressure as a Function of Temperature 

##### Update May 19, 2021: I have added a feature that generates a table of values from the graph (outputs temperature in degrees °C and pressure in mmHg). Bugs may still occur. If you get an error after inputting values up until C, it most likely will resolve itself once a C value is inputted.

Generating graphs of vapour pressure vs. tempearture graphs using Antoine's equation. The app can be viewed [here](https://share.streamlit.io/thomaslee01/vapourpressuregraph/Antoine_Graph.py) and was developed using Python for the backend, [Streamlit](https://streamlit.io/) for the front end and [Bokeh](https://bokeh.org/) for the graph generations. There still may be a few bugs that made it past me but so far everything is working okay. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r /path/to/requirements.txt
```

## Usage

### Windows 10:

Ensure that you have dependencies installed from requirements.txt above and from the directory of streamlit_app.py, open cmd.exe and enter the following:

```bash
streamlit run Antoine_Graph.py
```
Unfortunately I do not own a MacOS based device and do not know how to run this on MacOS. 

## Example 
Below is an example of how to use the app itself when viewed [here](https://share.streamlit.io/thomaslee01/vapourpressuregraph/Antoine_Graph.py) or through a
local server through localhost.

https://user-images.githubusercontent.com/51377707/118380520-529fad80-b5b0-11eb-99b0-29658ff9962f.mp4

### Image of the Downloaded Plot:
![bokeh_plot](https://user-images.githubusercontent.com/51377707/118383936-6b1fc000-b5d0-11eb-8e0f-b9596c34f182.png)

### Table of Values: 
![Screenshot from 2021-05-19 11-05-46](https://user-images.githubusercontent.com/51377707/118836847-42c6e880-b892-11eb-9a77-66059c04b793.jpg)


The example above showcased the values of Acetaldehyde and were retrieved from Table B.4 of [Elementary Principals of Chemical Processes 4th Ed. by Richard M. Felder](https://www.wiley.com/en-ca/Elementary+Principles+of+Chemical+Processes%2C+4th+Edition-p-9781119192107)

### Features to be Added (subject to change):

- Variety of units for temperature and pressure
- Ability to change the visuals of the graph
