import argparse
from .analengine import run_analysis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run data analytics on a specified dataset.")
    parser.add_argument("--api_key", type=str, help="Riot Games API key.", default="RGAPI-3074b506-5569-4d50-940c-099233ac3560")
    parser.add_argument("--summoner", type=str, required=True, help="Gamertag/Summoner name to analyze matches of.")
    parser.add_argument("--tag", type=str, required=True, help="Tag of summoner.")
    args = parser.parse_args()

    run_analysis(args.summoner, args.tag, "na1", args.api_key)
