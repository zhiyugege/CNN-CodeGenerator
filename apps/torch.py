class torch:
    
    def __init__(self,in_channels):
        
        self.code = ['import torch.nn as nn','import torch','class Net(nn.Module):','def __init__(self, in_channels='+in_channels+'):','super(Net, self).__init__()']    
        self.forward = ['def forward(self,input):']
        self.Conv2dNum = 1
        self.maxpoolNum = 1
        self.avgpoolNum = 1
        self.BNNum = 1
        self.fcNum = 1
        self.activeNum = [1,1,1,1,1,1]
        self.concatNum = 1

    def Conv2d(self,in_channels, out_channels, kernel_size, stride, padding, inputs):
        
        line = 'self.conv2d_'+str(self.Conv2dNum)
        line += ' = nn.Conv2d('+in_channels+', '+out_channels+', '+kernel_size+', stride='+stride+', padding='+padding+')'
        outputs = 'conv2d_'+str(self.Conv2dNum)+'_out'
        forward_line = outputs+' = self.conv2d_'+str(self.Conv2dNum)+'('+inputs+')'
        self.code.append(line)
        self.forward.append(forward_line)
        self.Conv2dNum += 1
        print(self.code)
        print(self.forward)
        return outputs

    def Pool2d(self,sign, kernel_size, stride, inputs):
        
        if sign=='maxpool':
            line = 'self.maxpool_'+str(self.maxpoolNum)+' = nn.MaxPool2d('+kernel_size+', stride='+kernel_size+')'
            outputs = 'maxpool_'+str(self.maxpoolNum)+'_out'
            forward_line = outputs+' = self.maxpool_'+str(self.maxpoolNum)+'('+inputs+')'
            self.maxpoolNum += 1
        else:
            line = 'self.avgpool_'+str(self.avgpoolNum)+' = nn.AvgPool2d('+kernel_size+', stride='+kernel_size+')'
            outputs = 'avgpool_'+str(self.avgpoolNum)+'_out'
            forward_line = outputs+' = self.avgpool_'+str(self.maxpoolNum)+'('+inputs+')'
            self.avgpoolNum += 1
        self.code.append(line)
        self.forward.append(forward_line)
        print(self.code)
        print(self.forward)
        return outputs

    def Activations(self, sign, inputs):
        

        if sign=='ReLU':
            line = 'self.ReLU = nn.ReLU()'
            outputs = 'ReLU_'+str(self.activeNum[0])+'_out'
            forward_line = outputs+' = self.ReLU('+inputs+')'
            self.activeNum[0] += 1
        elif sign== 'ELU':
            line = 'self.ELU = nn.ELU()'
            outputs = 'ELU_'+str(self.activeNum[1])+'_out'
            forward_line = outputs+' = self.ELU('+inputs+')'
            self.activeNum[1] += 1
        elif sign=='PReLU':
            line = 'self.PReLU = nn.PReLU()'
            outputs = 'PReLU_'+str(self.activeNum[2])+'_out'
            forward_line = outputs+' = self.PReLU('+inputs+')'
            self.activeNum[2] += 1
        elif sign== 'Sigmoid':
            line = 'self.Sigmoid = nn.Sigmoid()'
            outputs = 'Sigmoid_'+str(self.activeNum[3])+'_out'
            forward_line = outputs+' = self.Sigmoid('+inputs+')'
            self.activeNum[3] += 1
        elif sign=='Tanh':
            line = 'self.Tanh = nn.Tanh()'
            outputs = 'Tanh_'+str(self.activeNum[4])+'_out'
            forward_line = outputs+' = self.Tanh('+inputs+')'
            self.activeNum[4] += 1
        elif sign=='Softmax':
            line = 'self.Softmax = nn.Softmax()'
            outputs = 'Softmax_'+str(self.activeNum[5])+'_out'
            forward_line = outputs+' = self.Softmax('+inputs+')'
            self.activeNum[5] += 1
        if line not in self.code:
            self.code.append(line)
            print(self.code)
        self.forward.append(forward_line)
        print(self.forward)
        return outputs
    
    def BatchNorm(self, features, inputs):
        
        line = 'self.bn_'+str(self.BNNum)+' = nn.BatchNorm2d('+features+')'
        outputs = 'bn_'+str(self.BNNum)+'_out'
        forward_line = outputs+' = '+'self.bn_'+str(self.BNNum)+'('+inputs+')'
        self.code.append(line)
        self.forward.append(forward_line)
        self.BNNum += 1
        print(self.code)
        print(self.forward)
        return outputs

    def Concat(self, inputs, dimension='0'):
        outputs = 'concat_'+str(self.concatNum)+'_out'
        _str = '('
        for i in range(len(inputs)-1):
            _str = _str+inputs[i]+','
        _str = _str+inputs[-1]+')'
        forward_line = outputs+' = '+'torch.cat('+_str+', '+dimension+')'
        self.concatNum += 1
        self.forward.append(forward_line)
        print(self.forward)
        return outputs
         
    
    def Fc(self, in_channels, out_channels, inputs):
        line = 'self.fc_'+str(self.fcNum)+' = nn.Linear('+in_channels+','+out_channels+')'
        outputs = 'fc_'+str(self.fcNum)+'_out'
        forward_line = outputs+' = '+'self.fc_'+str(self.fcNum)+'('+inputs+')'
        self.fcNum += 1 
        self.code.append(line)
        self.forward.append(forward_line)
        print(self.code)
        print(self.forward)
        return outputs

    def Return(self, outputs):
        self.forward.append('return '+outputs)
# func = Torch()

# print(func.Conv2d('10','24','3','1','1'))
# print(func.Pool2d('maxpool','3','1'))
# print(func.BatchNorm('100'))
# print(func.Concat(['x','y'],'1'))
# print(func.Fc('1000','20'))
           
            
            
            
            