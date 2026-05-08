# Install / verify conda version
Install conda by following https://docs.conda.io/projects/conda/en/stable/user-guide/install/macos.html
`conda --version` # at least 24.5.0
# Python environment setup
- `conda create --name boca`
- `conda activate boca`
- conda install pip click
- pip install eventbrite requests pytest

# Setup API keys

## Eventbrite
Get the Eventbrite API key from https://www.eventbrite.com/myaccount/apps/
Export the Private token as an environment variable: 
export EVENTBRITE_TOKEN=<token>

## Zeffy
Get the Zeffy API key from https://www.zeffy.com (Organization Settings > API)
Export the API key as an environment variable:
export ZEFFY_API_KEY=<key>

# Run the program

## Eventbrite
`python3 src/main.py eventbrite` then enter order ID to print tickets.

## Zeffy
```bash
# Search by attendee name or email
python3 src/main.py zeffy --search "name"

# By payment ID
python3 src/main.py zeffy --payment-id <UUID>

# By ticket ID
python3 src/main.py zeffy --ticket-id <UUID>

# Dry run (no printing)
python3 src/main.py zeffy --search "name" --dry-run
```

# Run tests
```bash
conda run -n boca env PYTHONPATH=src python -m pytest tests/ -v
```

# Install ttf font
cd src
ipython
from tagswa.boca_printer import BocaTcpPrinter
boca = BocaTcpPrinter()
boca.download_ttf_font('../fonts/jf-openhuninn-2.0.ttf', 1)
# Wait until the LCD on boca printer showed "download ok" and "programming ok"
# This can take 3~5 minutes.

WHITE SIDE UP WHILE PUTTING PAPER IN
