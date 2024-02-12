Get the Eventbrite API key from https://www.eventbrite.com/myaccount/apps/
Export the Private token as an environment variable: export EVENTBRITE_TOKEN=<token>

Run: `python3 src/main.py eventbrite` then enter order ID to print tickets.

TODO:
- print individual ticket by barcode number
- reverse printing order
- keep track of printed tickets
- add tests