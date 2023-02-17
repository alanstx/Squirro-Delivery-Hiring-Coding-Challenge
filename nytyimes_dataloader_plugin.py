import argparse
import logging
import os

import requests

"""
Skeleton for Squirro Delivery Hiring Coding Challenge
August 2021
"""

log = logging.getLogger(__name__)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    def __init__(self, args_parser):
        self.args_parser = args_parser
        self.args = argparse.Namespace(**vars(args_parser.parse_args()), api_key=os.getenv("NYTIMES_APIKEY"))
        self._validate_query_params()
        self._handle_command_line_arguments()

    def connect(self, inc_column=None, max_inc_value=None):
        # NYTimes API does not require session handling or any such things
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def _validate_query_params(self):
        # https://developer.nytimes.com/docs/articlesearch-product/1/routes/articlesearch.json/get
        query_params = {
            "api-key",
            "begin_date",
            "end_date",
            "facet",
            "facet_fields",
            "facet_filter",
            "fl",
            "fq",
            "page",
            "query",
            "sort"
        }
        params = {key: value for key, value in self.args.__dict__.items() if key in query_params}
        params["api-key"] = self.args.__dict__.get("api_key")
        if "page" not in params:
            params["page"] = 0

        if params["api-key"] is None:
            raise Exception("Parameter 'api-key' is required to perform api requests to the 'nytimes.com'")

        if unsupported_params := set(params).difference(query_params):
            log.warning(f"Following query params might be unsupported: {', '.join(unsupported_params)}")

        self.query_params = params

    def _handle_command_line_arguments(self):
        if getattr(self.args, "schema"):
            self.getSchema()
        if getattr(self.args, "arguments"):
            self.getArguments()

    def _handle_request(self):
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

        response = requests.get(url, params=self.query_params)
        if response.status_code == 401:
            raise Exception("Unauthorized request. Make sure api-key is set.")
        elif response.status_code == 429:
            raise Exception("Too many requests. You reached your per minute or per day rate limit.")

        return response.json()

    @staticmethod
    def _flatten_dict(source_dict):
        new_dict = {}
        while source_dict:
            for key, value in list(source_dict.items()):
                if isinstance(value, dict):
                    temp_value = source_dict.pop(key)
                    for inner_key, inner_value in temp_value.items():
                        source_dict[f"{key}.{inner_key}"] = temp_value[inner_key]
                else:
                    new_dict[key] = source_dict.pop(key)
        return new_dict

    def getRecords(self, batch_size):
        temp_batch_size = batch_size
        while temp_batch_size > 0:
            response = self._handle_request()
            articles = response["response"]["docs"]
            for article in articles:
                yield self._flatten_dict(article)
            temp_batch_size -= len(articles)
            self.query_params["page"] += 1

    def getDataBatch(self):
        """
        Generator - Get data from source on batches.

        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        """
        batch_size = self.args.batch_size

        rows = []
        for row in self.getRecords(batch_size):
            rows.append(row)
            if len(rows) >= batch_size:
                yield rows
                rows = []
        yield rows

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """
        if _item := next(self.getRecords(1)):
            result = list(_item.keys())
            # Remove print if unnecessary
            print(result)
            return result
        return []

    @staticmethod
    def getArguments():
        """
        Get required or optional arguments to use with the dataloader plugin

        Depends of the requirements but in theory this list could be
        dynamically generated based on the argparse.ArgumentParser class (self.args_parser)
        """
        arguments = [
            {
                "name": "--batch_size",
                "help": "Number of NYTimes articles to load",
                "required": False,
                "default": 10,
                "type": "int",
            },
            {
                "name": "--schema",
                "help": "Return the schema of the dataset",
                "required": False,
                "default": False,
                "type": "bool",
            },
            {
                "name": "--arguments",
                "help": "Get arguments that can be used with the dataloader plugin",
                "required": False,
                "default": False,
                "type": "bool",
            },
            {
                "name": "--query",
                "help": "Query to the NYTimes Articles API",
                "required": True,
                "default": "Silicon Valley",
                "type": "str",
            },
            {
                "name": "--page",
                "help": "Page from where to start requesting NYTimes Articles API",
                "required": False,
                "default": 0,
                "type": "int",
            },
        ]
        # Remove print if unnecessary
        print(arguments)
        return arguments


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NYTimes dataloader plugin (codding challenge)")
    parser.add_argument("--batch_size", type=int, help="How many articles to get", default=10)
    parser.add_argument("--schema", help="Return the schema of the dataset", action="store_true")
    parser.add_argument(
        "--arguments", help="Get arguments that can be used with the dataloader plugin", action="store_true"
    )
    parser.add_argument("--query", type=str, help="Query to the NYTimes Articles API", default="Silicon Valley")
    parser.add_argument("--page", type=int, help="Page from where to start requesting NYTimes Articles API", default=0)

    source = NYTimesSource(args_parser=parser)

    for idx, batch in enumerate(source.getDataBatch()):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(f"  - {item['_id']} - {item['headline.main']}")
