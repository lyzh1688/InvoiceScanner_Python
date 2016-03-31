from scan.algorithm.RunLengthAlgo.RunLenAction import RunLenAction

class ScanAlgoFactory(object):

    @staticmethod
    def scan(algo,file,type):
        algoName = algo + 'Action'
        return eval(algoName)(file,type)