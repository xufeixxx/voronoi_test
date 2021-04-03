class Settings:

    def __init__(self):
        self.map_width = [0, 500]
        self.map_length = [0, 500]
        self.point_num = 10


"""
根据实验记录，点数为20的时候，不是全部封闭维诺个的比例大约是0.4还是比较高的
200 ---> 0.07
2000 ----> 0.011
20000 ----> 0.008
由此可见当使用上百万的数据点（道路交叉口）时，数据小的可以忽略不计了，所以本模型只记录封闭性维诺格
只计算用户位置信息在封闭维诺格中的数据,不在封闭维诺格中的位置信息不去计算.vor.regions某一项有-1的话说明不封闭
"""
