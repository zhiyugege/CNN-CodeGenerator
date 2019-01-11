class torch:
    
    def __init__(self,in_channels):
        
        self.code = ['import torch.nn as nn','import torch','class Net(nn.Module):','def __init__(self, in_channels='+in_channels+'):','super(Net, self).__init__()']    
        self.Conv2dNum = 1;
        self.maxpoolNum = 1;
        self.avgpoolNum = 1;
        self.BNNum = 1;
        self.fcNum = 1;

    def Conv2d(self,in_channels, out_channels, kernel_size, stride, padding):
        
        line = 'self.conv2d'+str(self.Conv2dNum)
        line += ' = nn.Conv2d('+in_channels+', '+out_channels+', '+kernel_size+', stride='+stride+', padding='+padding+')'
        self.code.append(line)
        self.Conv2dNum += 1
        print(self.code)

    def Pool2d(self,sign, kernel_size, stride):
        
        if sign=='maxpool':
            line = 'self.maxpool'+str(self.maxpoolNum)+' = nn.MaxPool2d('+kernel_size+', stride='+kernel_size+')'
            self.maxpoolNum += 1
        else:
            line = 'self.avgpool'+str(self.avgpoolNum)+' = nn.AvgPool2d('+kernel_size+', stride='+kernel_size+')'
            self.avgpoolNum += 1
        self.code.append(line)
        print(self.code)

    def Activations(self, sign):
        

        if sign=='ReLU':
            line = 'self.ReLU = nn.ReLU()'
        elif sign== 'ELU':
            line = 'self.ELU = nn.ELU()'
        elif sign=='PReLU':
            line = 'self.PReLU = nn.PReLU()'
        elif sign== 'Sigmoid':
            line = 'self.Sigmoid = nn.Sigmoid()'
        elif sign=='Tanh':
            line = 'self.Tanh = nn.Tanh()'
        elif sign=='Softmax':
            line = 'self.Softmax = nn.Softmax()'
        if line not in self.code:
            self.code.append(line)
            print(self.code)
    
    def BatchNorm(self, features):
        
        line = 'self.bn'+str(self.BNNum)+' = nn.BatchNorm2d('+features+')'
        self.code.append(line)
        self.BNNum += 1
        print(self.code)

    def Concat(self, inputs, dimension='0'):
        _str = '('
        for i in range(len(inputs)-1):
            _str = _str+inputs[i]+','
        _str = _str+inputs[-1]+')'
        line = 'self.concat = torch.cat('+_str+', '+dimension+')'
        self.code.append(line)
        print(self.code)
    
    def Fc(self, in_channels, out_channels):
        line = 'self.fc'+str(self.fcNum)+' = nn.Linear('+in_channels+','+out_channels+')'
        self.fcNum += 1 
        self.code.append(line)
        print(self.code)
# func = Torch()
# print(func.Conv2d('10','24','3','1','1'))
# print(func.Pool2d('maxpool','3','1'))
# print(func.BatchNorm('100'))
# print(func.Concat(['x','y'],'1'))
# print(func.Fc('1000','20'))
           
            
            
            
            