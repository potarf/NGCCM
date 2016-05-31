
#Should be a robust interpreter of basic test scripts
basics = {
    "SR":"",
    "CR":"",
    "SW":"",
    "CW":""
         }

userSeqs = dict()

def ex(statement):
    if statement in basics.keys():
        print "I should call %s now" %statement
    elif statement in userSeqs.keys():
        print "I should call %s now" %statement
    else:
        print "ERROR: %s not known" % statement
    return

def defineSeq(lines):
    name = "KevinBacon"
    userSeqs[name]["cmds"] = list()
    #Line 1 has name and list of args
    for item in lines:
        userSeqs[name]["cmds"].append(item)
    #Rest of lines go in list of commands
    #Store in dict
ex("SW")
ex("KevinBacon")
userSeqs["KevinBacon"] = ""
ex("KevinBacon")
