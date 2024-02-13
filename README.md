# Automatic Painting by Numbers

Automatic Painting by Numbers is a Python application that utilizes the Dobot Magician robotic arm to 
automatically connect dots in the correct order and fill in areas.

## Prerequisites
To run the application you need the following equipment:
- Dobot Magician
- Webcam or Camera

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt
```

Set up [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) by installing the software 
and then include the executable path in the app.py file as follows:

```python
PYTESSERACT_PATH = "C:/Your/Example/Path/tesseract.exe"
```

To enable homing of the Dobot Magician, install 
[Dobotstudio](https://www.dobot-robots.com/products/education/magician.html) and utilize its software.

## Usage

Specify the correct port for the Dobot Magician and customize other settings to your preferences in 
app.py.
```python
DOBOT_PORT = <YOUR_PORT>
```

Enable the desired use case by uncommenting the relevant code within the run function of app.py. 
For example, to run the first use case, comment/uncomment the following code:
```python
# Runs the first use case to draw dot to dot
run_dot_to_dot()

# Runs the second use case to color areas
# run_fill_areas()
```
Run the application by executing the file `__main__.py`.

## Authors
This project was developed in the context of the course "Applied Robotics" at Hochschule Hof, 
University of Applied Sciences.
- Patrick Schröder
- Marina Waller
- Gleb Hubarevich
- Denys Zarishniuk

GitHub: https://github.com/bypschroeder/AutoPainter
