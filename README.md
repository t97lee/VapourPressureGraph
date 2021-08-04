# Graphing Vapour Pressure as a Function of Temperature 

|Date   |Update   |
|----|---|
|<img width=200/>June 2   |Added feature to change temperature units for the graph. Apologies for the spaghetti code - I'll revisit and refactor when I get the chance to. |
|May 27   |Added a feature to select different pressure units added (bar, kPa, atm, mmHg). Will incorporate an option to select different temperature units in the near future. I am also refactoring the source code to include classes and such to clean up the messy code. |
|May 24   |A feature that allows users to download an .xlsx spreadsheet from the table of values has been added. |
|May 19   |I have added a feature that generates a table of values from the graph (outputs temperature in degrees °C and pressure in mmHg). Bugs may still occur. If you                    get an error after inputting values up until C, it most likely will resolve itself once a C value is inputted. |
 
### Generating graphs of vapour pressure vs. tempearture graphs using Antoine's equation. The app can be viewed [here](https://share.streamlit.io/thomaslee01/vapourpressuregraph/Antoine_Graph.py) and was developed using Python for the backend, [Streamlit](https://streamlit.io/) for the front end and [Bokeh](https://bokeh.org/) for the graph generations.

## Installation

Clone the repository using:

```bash
git clone https://github.com/thomaslee01/VapourPressureGraph
```

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

## Example (outdated, will update soon)
Below is an example of how to use the app itself when viewed [here](https://share.streamlit.io/thomaslee01/vapourpressuregraph/Antoine_Graph.py) or through a
local server through localhost.


https://user-images.githubusercontent.com/51377707/121049688-f0d4fc80-c785-11eb-8bc9-bef9d2cd8a86.mp4


### Image of the Downloaded Plot:
![bokeh_plot](https://user-images.githubusercontent.com/51377707/118383936-6b1fc000-b5d0-11eb-8e0f-b9596c34f182.png)

### Table of Values: 
![Screenshot from 2021-05-19 11-05-46](https://user-images.githubusercontent.com/51377707/118836847-42c6e880-b892-11eb-9a77-66059c04b793.jpg)


The example above showcased the values of Acetaldehyde and were retrieved from Table B.4 of [Elementary Principals of Chemical Processes 4th Ed. by Richard M. Felder.](https://www.wiley.com/en-ca/Elementary+Principles+of+Chemical+Processes%2C+4th+Edition-p-9781119192107)

### Things to update:
- Include docstrings for classes and functions 
- Refactoring code, the functions are very very ugly to edit and look at. 
- Layout changes, move the graph to the right of the web app instead of having it hanging at the bottom. 
- Update graph line legend (blue line) to reflect the pressure units seleteced. 
- Change file type to .csv
