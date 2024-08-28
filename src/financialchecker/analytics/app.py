import argparse
from datetime import date

import plotly.express as px

from financialchecker.data.aggregate import DataAggregate


def main():
    parser = argparse.ArgumentParser("Financial Checker Analytics")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    transaction_parser = subparsers.add_parser(name="transaction",
                                               help="Transaction related commands")
    transaction_parser.add_argument("-t",
                                    "--type",
                                    choices=["all", "expenses", "income"],
                                    default="all")
    transaction_parser.add_argument("-s",
                                    "--start",
                                    type=str,
                                    help="Starting date format (%Y-%m-%d)",
                                    default=date.today().strftime("%Y-%m-%d"))
    transaction_parser.add_argument("-e",
                                    "--end",
                                    type=str,
                                    help="Starting end format (%Y-%m-%d)",
                                    default=date.today().strftime("%Y-%m-%d"))
    transaction_parser.add_argument("-c",
                                    "--category",
                                    type=str,
                                    help="Select the category")
    transaction_parser.add_argument("-pt",
                                    "--plot-type",
                                    choices=["dist", "distribution"],
                                    default="dist")
    transaction_parser.add_argument("-f",
                                    "--file",
                                    type=str,
                                    help="Storing folder",
                                    default="./result.png")

    args = parser.parse_args()

    match args.command:
        case "transaction":
            print(f"Transaction Type selected -> {args.type}")
            print(f"From -> {args.start}")
            print(f"To -> {args.end}")
            print(f"Category -> {'all' if not args.category else args.category}")
            print(f"Plot Type -> {args.plot_type}")
            print(f"Storing -> {args.file}")

            aggregator = DataAggregate()

            match args.type:
                case "income":
                    fig = px.histogram(aggregator.get_income_amount_distribution())
                    fig.write_image(args.file)
                case "expense":
                    fig = px.histogram(aggregator.get_expense_amount_distribution())
                    fig.write_image(args.file)
                case "all":
                    print("No plot visualization is available")


if __name__ == "__main__":
    main()
