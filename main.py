import argparse
import atexit
from batchelor import Batchelor


parser = argparse.ArgumentParser(description="Makes sure you are the most eligible batchelor")
parser.add_argument("url", type=str, nargs=1, help="The URL to the tab page where the vote is held")
parser.add_argument("name", type=str, nargs=1, help="The batchelor you wish to vote for")
parser.add_argument("margin", type=float, nargs=1, help="The percentage margin you wish to maintain as a decimal, e.g. 0.2 for 20%")


batchelor_run = Batchelor(
	"https://thetab.com/uk/exeter/2019/03/07/vote-for-exeters-most-eligible-bachelor-heat-three-2-41350",
	"Hugo",
	0.2
)

batchelor_run.start()

def exit_handler():
	batchelor_run.close_driver()


atexit.register(exit_handler)