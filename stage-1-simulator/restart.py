import sys
import pandas as pd
import json as js

import simulator

if __name__ == "__main__":
    if len(sys.argv) == 1:
        simulator.restart()
