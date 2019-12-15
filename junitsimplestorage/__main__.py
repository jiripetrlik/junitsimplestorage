import argparse

import junitsimplestorage

if __name__ == "__main__":
    # Read configuration from commad line arguments
    parser = argparse.ArgumentParser(description = "JUnit Simple Storage")
    parser.add_argument("-d", "--database", required=False, help="SQL database URI", type=str)
    parser.add_argument("-e", "--echo-sql", action="store_true", required=False, help="Echo SQL queries")
    args = parser.parse_args()
    config = {}
    if args.database != None:
        config["SQLALCHEMY_DATABASE_URI"] = args.database
    if args.echo_sql == True:
        config["SQLALCHEMY_ECHO"] = args.echo_sql

    app = junitsimplestorage.create_app(config)
    app.run()