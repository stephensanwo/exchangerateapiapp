# Exchange-Rate-Analytics

Exchange rate API is an experimental API created to provide historical
and predicted exchange rate data for the Naira (NGN) against three
currencies, USD, EUR and GBP. <br />

The API architecture is best explained with the illustration below. In
summary, historical data is scraped from BDC websites which release only
about a week old live data on their websites, and do not provide an open
source API for third parties to access the historical rates for
analysis.
<br />
The data is stored in a mongodb cloud atlas storage, and forms the core
json data for the historical rates requests via the API routes.
<br />The data is then used to make a 30 day rate forecast, leveraging
Facebook's open sourced forecasting model.The forecast result is
available via a get request.

Read the full documentation here : "https://documenter.getpostman.com/view/7844749/SzKPW2AY"
