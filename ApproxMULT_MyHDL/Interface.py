import json

class Col:
    def __init__(self, col):
        # data for current stage's inputs
        self.col_len = col["col_len"];
        if col["remainingBits"] is None:
            self.rbs = [];
        else:
            self.rbs = col["remainingBits"];
        if col["AC42"] is None:
            self.ac42 = [];
        else:
            self.ac42 = col["AC42"];
        if col["AC32"] is None:
            self.ac32 = [];
        else:
            self.ac32 = col["AC32"];
        if col["F"] is None:
            self.f = [];
        else:
            self.f = col["F"];
        if col["H"] is None:
            self.h = [];
        else:
            self.h = col["H"];
        # data from last stage's outputs
        self.nRbs_out = col["outRemainingBitsNum"];
        self.nAC42_out = col["outAC42BitsNum"];
        self.nAC32_out = col["outAC32BitsNum"];
        self.nF_out = col["outFBitsNum"];
        self.nH_out = col["outHBitsNum"];
        self.nFC_out = col["outFcBitsNum"];
        self.nHC_out = col["outHcBitsNum"];


    
def ParseJson(JsonName):
    file = open(JsonName,'r');
    js = file.read();
    CompressorTree = json.loads(js);
    Stages = [];
    for i in range(len(CompressorTree)):
        stage = CompressorTree["stage"+str(i)];
        Stage = [];
        for j in range(len(stage)):
            col = stage[j];
            Stage.append(Col(col));
        Stage.reverse();
        Stages.append(Stage);
    return Stages;

