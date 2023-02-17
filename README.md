## Readme
NYTimes Data Loader Plugin - Squirro Delivery Hiring Coding Challenge.

## Dependencies
Placed in `requirements.txt`

## Initial setup
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `NYTIMES_APIKEY` should not be hardcoded in the code but loaded from a secure place. The plugin supports loading dynamically from the environment variable. We simulate this behavior in the commands below. 

Instead of adding an apikey to each command, we can of course do something like this just once:
`export NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx'`
And then in all commands we can omit adding api key.

## Usage
```
# Get 1 batch of results for default query
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py

# Print and return the schema of the dataset
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py --schema

# Print and return required or optional arguments to use with the dataloader plugin
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py --arguments

# Return batch of default size for the query 'Husky' from the NYTimes API data source
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py --query 'Husky'

# Return batch of the specified size for the query 'Husky' from the NYTimes API data source.
# If the data source returned more items than the batch_size,
# the rest of the items will be returned in the next batch, smaller than the batch_size.
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py --query 'Husky' --batch_size 16

# By default, the data loader paginates through the API results as long as it gets 
# enough items to the batch_size. We can specify from which page to start.
NYTIMES_APIKEY='jihIUgAfNcWnUKU3L0PazRcEW6cdCZTx' python3 nytyimes_dataloader_plugin.py --query 'Husky' --page 4
```

## Useful sources
### Squiro docs
- https://squirro.atlassian.net/wiki/spaces/DOC/pages/30670956/DataSource+Class
- https://docs.squirro.com/en/latest/technical/data-loading/plugins/example-plugin.html
- https://docs.squirro.com/en/latest/technical/data-loading/plugins/boilerplate.html
- https://docs.squirro.com/en/latest/technical/data-loading/how-to/custom-connector.html
- https://docs.squirro.com/en/latest/technical/data-loading/data-loader.html

### NYTimes API docs
- https://developer.nytimes.com/docs/articlesearch-product/1/routes/articlesearch.json/get