# Development Guide

## Conda Environment

This project uses the `boca` conda environment.

## Running Tests

```bash
conda run -n boca env PYTHONPATH=src python -m pytest tests/ -v
```

`PYTHONPATH=src` is required because all imports are relative to the `src/` directory.

## Running the CLI

```bash
# Eventbrite
conda run -n boca env PYTHONPATH=src python src/main.py eventbrite --order_id <ORDER_ID> --dry-run

# Zeffy — search by name
conda run -n boca env PYTHONPATH=src python src/main.py zeffy --search "name" --dry-run

# Zeffy — by payment or ticket ID
conda run -n boca env PYTHONPATH=src python src/main.py zeffy --payment-id <UUID> --dry-run
conda run -n boca env PYTHONPATH=src python src/main.py zeffy --ticket-id <UUID> --dry-run
```

## Architecture

Three layers:
- **Data source**: `EventbriteManager`, `ZeffyManager` — platform-specific API clients
- **Rendering**: `Ticket` ABC > layout classes (one per venue) > concrete event tickets
- **Printer**: `BocaTcpPrinter` / `BocaNullPrinter`

Layout = venue. Each layout class owns `ORG_TITLE`, `VENUE_TITLE`, `VENUE_ADDR` as class constants.

## Environment Variables

- `EVENTBRITE_TOKEN` — required for the `eventbrite` command
- `ZEFFY_API_KEY` — required for the `zeffy` command

## Adding a New Zeffy Event

1. Create a new ticket class in `src/tagswa/` inheriting from `Ticket`
2. Set `EVENTID` to the Zeffy campaign UUID
3. Set `ORG_TITLE`, `VENUE_TITLE`, `VENUE_ADDR` class constants
4. Add the class to `ZEFFY_TICKET_CLASSES` list in `src/main.py`
