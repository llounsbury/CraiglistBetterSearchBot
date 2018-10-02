# CraiglistBetterSearchBot

This is a proof of concept script which uses Selenium automation to provide better more refined search results when using Craigslist.

## How to use:
1. Install geckodriver and place in Path (/usr/local/path)

2. Create python env with the latest version of selenium

3. Set the CRAIGSLISTPAGE variable to a search, eg in this case all motorcycles posted today within 2000 miles of Iowa City Iowa.
Terms meeting this criteria are listed. 

4. Set terms to look for, and terms to avoid

5. If you wish to see contact info in your results, uncomment line 76. This will slow down results by attempting to open the captcha hiding phone numbers, names and emails.

6. Run the script. Example results provided as Results.jpg


As the intent of this program is to eventually create a notifier when items are posted, a "Would notify user" tag is added to posts that meet all critera of search keys and avoid list
