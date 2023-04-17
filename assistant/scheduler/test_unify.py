import pytest

from assistant.scheduler.unification import *

# unification( "?x", "Fred")
# unification( "Fred", "Fred")
# unification( "Fred", "Barney")
# unification(["son", "Barney", "?y"], ["son", "Barney", "Bam-Bam"])
# unification(["son", "?x", "Bam-Bam"], ["son", "Barney", "?x"])
# unification(["son", "?x", "Bam-Bam"], ["son", "Barney", "?y"])
# unification(["son", "?x", "Bam-Bam"], ["son", "Barney", "?y"])
# unification(["son", "?x", "Bam-Bam"], ["son", "Barney", "?x"])
# unification(["son", "Barney", "Bam-Bam"], ["son", "Barney", "?y"])
# unification(["son?", "Barney", "?x"], ["son?", "?y", ["son", "Barney"]])
# unification(["son?", "Barney", "?x"], ["son?", "?y", ["son", "?y"]])
# unification( ["loves", "?x", "?y"], ["loves", "Fred", "Wilma"])
# unification( ["loves", "?x", "Wilma"], ["loves", "Fred",  "?y"])
# unification( ["loves", "?x", "Wilma"], ["loves", "Fred",  "?x"])

#print( unify( "?x", "Wilma"))
#print( unify( "(loves ?x ?x)", "(loves Wilma Fred)"))
#print( unify( "(loves (leftLegOf ?x) (rightLegOf Wilma))", "(loves (leftLegOf Wilma) (rightLegOf ?y))"))
#print( unify( '(father Barney ?x)', '(father Barney (son_of Barney))'))
