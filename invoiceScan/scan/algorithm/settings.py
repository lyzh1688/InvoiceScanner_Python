__author__ = 'Yuezhi.Liu'
RUN_LEN_THRESHOLD = \
{
    'DEFAULT':{
            'GRAY_THRESH':190,
            'BLOCK_SIZE':51,
            'MINUS_PARAM':10,
            #filer the vertical and horizantal line
            'MaxRLWidth':10,
            'MaxRLHeight':30,
            'MaxStrokNum':3,
            'MaxRLDistance':10,
            'MinRLDistance':10,
            'HJoinMax':10,
            'VJoinMax':3,
            'MinHeight':3,
            'H_Offset':5,
            'V_Offset':5,
            #img resize
            'ROW':400,
            'COL':600,
        }
}