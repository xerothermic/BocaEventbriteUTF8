### Time:
 02/11/2024 ~ 05/27/2024 (Memorial day)

### Lessons:
1. 02/11/2024: Print tickets
2. 02/17/2024 (in Vancouver, may need makeup class)
3. 02/24/2024 (in Vancouver, may need makeup class)
4. 03/02/2024
5. 03/09/2024
6. 03/16/2024
7. 03/23/2024
8. 03/30/2024
9. 04/06/2024
10. 04/13/2024
11. 04/20/2024
12. 04/27/2024
13. 05/04/2024
14. 05/11/2024
15. 05/18/2024 (Hummingbird performance, may need makeup class)
16. 05/25/2024 

### Deliverables
1. Print tickets
2. Make small tweaks (fix small problems. Add small features)
    1. print based on barcode number
    2. remove extra space in order_id
    3. create new event template
3. Search tickets
4. Create ticket for new customer
5. Refund ticket for existing customer
6. How to setup Boca Printer

## Lesson notes:
02/11/2024: print tickets
To print tickets, we need to know a few variables.
1. Eventbrite API key
2. order_id


### Get eventbrite API key:
1. Goto: https://www.eventbrite.com/account-settings/apps
2. Copy private token
3. Open a terminal (cmd+shift+p --> Terminal: Create New Terminal (In Active workspace))
4. `export EVENTBRITE_TOKEN=<paste token from step2>`

### Get order_id: 6371870169 (In NOTES.txt for testing)

### print ticket in --dry-run mode
Use this when not connecting to the actual printer.
1. In the same terminal where eventbrite API key has been setup
2. `python src/main.py eventbrite --dry-run` (use --dry-run when the printer is not connected to test the program)
3. paste order_id
4. see what happened :D 

The expected results are
```
boca) (base) patlu@Patricks-MacBook-Pro BocaEventbriteUTF8 % python src/main.py eventbrite --dry-run
Enter your order id: 6371870169
2024-02-11 18:03:35,261 main.py eventbrite:67 - INFO - Sending 0 to printer
2024-02-11 18:03:35,261 boca_printer.py print:15 - INFO - Received:<RC0,65><TTF1,8>Taiwanese Association of Greater Seattle 大西雅圖台灣同鄉會<TTF1,12><RC70,65>Taiwan Reminiscence by Taiwan Acrobatic<RC130,65>Troupe 【台灣追想曲】台灣特技團<F3><RC215,65>Meydenbauer Center<RC265,65>11100 Northeast 6th Street, Bellevue, WA 98004<RC315,65>Fri May 19 19:00:00 2023 - Fri May 19 21:00:00 2023<RC365,65>$50.00<RC440,65><TTF1,8>國清 甄<RC490,65>Premium, Section: C, Row: A, Seat: 107<F3><RC0,1200>#6371870169<RC0,1500>#6371870169<RC40,1500>Premium<RC135,1500>Section: C<RC170,1500>Row: A<RC205,1500>Seat: 107<RC265,1500><QR5>{637187016910378621839001}<RC505,1500><F2>637187016910378621839001<p>
2024-02-11 18:03:36,390 main.py eventbrite:67 - INFO - Sending 1 to printer
2024-02-11 18:03:36,390 boca_printer.py print:15 - INFO - Received:<RC0,65><TTF1,8>Taiwanese Association of Greater Seattle 大西雅圖台灣同鄉會<TTF1,12><RC70,65>Taiwan Reminiscence by Taiwan Acrobatic<RC130,65>Troupe 【台灣追想曲】台灣特技團<F3><RC215,65>Meydenbauer Center<RC265,65>11100 Northeast 6th Street, Bellevue, WA 98004<RC315,65>Fri May 19 19:00:00 2023 - Fri May 19 21:00:00 2023<RC365,65>$50.00<RC440,65><TTF1,8>國清 甄<RC490,65>Premium, Section: C, Row: A, Seat: 111<F3><RC0,1200>#6371870169<RC0,1500>#6371870169<RC40,1500>Premium<RC135,1500>Section: C<RC170,1500>Row: A<RC205,1500>Seat: 111<RC265,1500><QR5>{637187016910378621879001}<RC505,1500><F2>637187016910378621879001<p>
```

### Add Attendees
1. Find the appropriate event from: https://www.eventbrite.com/organizations/events/ (if not able to find your event, change to show all event)
2. click "manage attenendees, then select add atendees
3. enter quantity and select order type


### Find order number
1. Find the appropriate event from: https://www.eventbrite.com/organizations/events/ (if not able to find your event, change to show all event)
2. click "manage attenendees, then select orders

### Find barcode number (for printing part of the order)
1. Find the appropriate event from: https://www.eventbrite.com/organizations/events/ (if not able to find your event, change to show all event)
2. click "manage attenendees, then select orders
3. find the order using search bar by providing name, email, etc.
4. click Actions next to the blue order number, then select "View Attendee Report"
5. Edit columns, then select "Barcode Number"
6. Scroll the bottom table to the right to see individual Barcode Number
