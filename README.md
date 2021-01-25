# scrape-website-table
Scrape and clean data from a table on a website.

Scrapes data from https://www.bluehawk.coop/our-co-op/our-member-locations by default, and cleans it up using `pandas` into a digestible format.

Functions as a command line tool; can provide a different link by using `--url` arugment, and specify location to save Excel file using `--loc` argument.