Get the Eventbrite API key from https://www.eventbrite.com/myaccount/apps/
Export the API key as an environment variable: EVENTBRITE_TOKEN

Run: `python3 main.py eventbrite` then enter order ID to print tickets.
For a different event, pass `--event_id <event id>` to the command line.

TODO:
- validate order ID with event ID (or extract event ID from order ID)
- reverse printing order
- keep track of printed tickets
- add tests