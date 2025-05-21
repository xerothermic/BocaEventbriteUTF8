# Python enviornment setup
- `conda create -n boca`
- `conda activate boca`
- conda install pip click
- pip install eventbrite

# Setup Eventbrite API key
Get the Eventbrite API key from https://www.eventbrite.com/myaccount/apps/
Export the Private token as an environment variable: 
export EVENTBRITE_TOKEN=<token>

# Run the program
Run: `python3 src/main.py eventbrite` then enter order ID to print tickets.


TODO:
- print individual ticket by barcode number
- reverse printing order
- keep track of printed tickets
- add tests

WHITE SIDE UP WHILE PUTTING PAPER IN
