#import sys
import read_files
import find_elements
import formula_NotNumber
import formula_SpecialChar

if __name__ == "__main__":

    dfGFA = read_files.loadGFA()
    dfElements = read_files.loadTablaPeriodica()
    #find_elements.findIndexPosition(dfGFA,dfElements)
    formula_SpecialChar.FormulaStarSpecialChar(dfGFA)


#    if len(sys.argv) == 1:
#        simulator.restart()
#    else:
#        simulator.restart(sys.argv[1])