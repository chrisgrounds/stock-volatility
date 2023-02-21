import datetime
import logging
from yahoo_fin import stock_info
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))

    stock_df = stock_info.get_data("TSLA")
    stock_df = stock_df.rename_axis("date").reset_index()

    num_rows = len(stock_df) - 1
    last_row = stock_df.iloc(-1)

    date = last_row["date"]
    adjclose = last_row["adjclose"]

    print(last_row)
    print(date)
    print(adjclose)

    dynamodb = boto3.client('dynamodb')

    dynamodb.put_item(
        TableName="stock_data",
        Item={
            "date": { "S": str(date) },
            "adjclose": { "S": str(adjclose) }
        }
    )

