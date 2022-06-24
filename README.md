# CDR-hypotenuse-calculation

## Description

This work is part of a research, where we started investigating how to use some compute methods to recognize parts of OCT images (using Deep Learning). The output segmentated is used in this work to find a way of locating some characteristics in specific regions.

These regions were used to compute a calculation, which consist of the Pythagoras theorem.

## Summary installs

1. Create a virtual environment inside main folder

    1.1. `python3 -m venv venv` → creates a virtual environment

    1.2. `venv\Scripts\activate.bat` → activates the environment (on windows with cmd) 
    
    1.3. (not req.) `deactivate` → deactivates the environment if is necessary

    1.4. `pip install -r requirements.txt` → for install all dependences

    1.5. (not req.) `pip freeze > requirements.txt` → when the development was to finish

## Issues

    → Maybe try to find another way to search some coordinates, read pixel per pixel is so much costly
    
    → Some pictures that I tested, don't perform correctly some coordinates

## Next steps

    → To find a way of reading a small part of each original image to know the right scale (in microns)
