import argparse
# from .analengine import run_analysis
from .analyzer import run_analysis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run data analytics on a specified dataset.")
    parser.add_argument("--api_key", type=str, help="Riot Games API key.", default="RGAPI-f98c9c45-17e7-464e-bb59-82cb1da5e837")
    parser.add_argument("--summoner", type=str, required=True, help="Gamertag/Summoner name to analyze matches of.")
    parser.add_argument("--tag", type=str, required=True, help="Tag of summoner.")
    args = parser.parse_args()

    analysis = run_analysis(args.summoner, args.tag, "na1", args.api_key)
    print(analysis)
