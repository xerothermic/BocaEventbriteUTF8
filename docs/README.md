# Install / verify conda version
Install conda by following https://docs.conda.io/projects/conda/en/stable/user-guide/install/macos.html
`conda --version` # at least 24.5.0
# Python enviornment setup
- `conda create --name boca`
- `conda activate boca`
- conda install pip click
- pip install eventbrite

# Setup Eventbrite API key
Get the Eventbrite API key from https://www.eventbrite.com/myaccount/apps/
Export the Private token as an environment variable: 
export EVENTBRITE_TOKEN=<token>

# Run the program
Run: `python3 src/main.py eventbrite` then enter order ID to print tickets.

# Install ttf font
cd src
ipython
from tagswa.boca_printer import BocaTcpPrinter
boca = BocaTcpPrinter()
boca.download_ttf_font('../fonts/jf-openhuninn-2.0.ttf', 1)
# Wait until the LCD on boca printer showed "download ok" and "programming ok"
# This can take 3~5 minutes.

TODO:
- print individual ticket by barcode number
- reverse printing order
- keep track of printed tickets
- add tests

WHITE SIDE UP WHILE PUTTING PAPER IN
