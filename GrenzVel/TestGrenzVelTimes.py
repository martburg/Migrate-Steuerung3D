print'PosSpline with Cython and Initialized Arrays Timing '
print 'TestGrenzVelTimes'
from numpy import linspace,amax,amin
from scipy.interpolate import splprep, splev, interp1d
from scipy.integrate import romberg

from math import sqrt
import time
import numpy as np

from GrenzVelTimes import GrenzVel

import matplotlib.pyplot as plt

#scipy.interpolate.splprep(x, w=None, u=None, ub=None, ue=None, k=3, task=0,
#                          s=None, t=None, full_output=0, nest=None, per=0, quiet=1)[source]

# Find the B-spline representation of an N-dimensional curve.

# Given a list of N rank-1 arrays, x, which represent a curve in N-dimensional space parametrized by u,
# find a smooth approximating spline curve g(u). Uses the FORTRAN routine parcur from FITPACK

#Parameters :	
#           x, y : array_like A list of sample vector arrays representing the curve.
#              w : array_like Strictly positive rank-1 array of weights the same length as x and y. 
#                             The weights are used in computing the weighted least-squares spline fit.
#                             If the errors in the y values have standard-deviation given by the vector d, then w should be 1/d.
#                             Default is ones(len(x)).
#         xb, xe : float      The interval to fit. If None, these default to x[0] and x[-1] respectively.
#              k : int        The order of the spline fit. It is recommended to use cubic splines.
#                             Even order splines should be avoided especially with small s values. 1 <= k <= 5
#           task : {1, 0, -1} If task==0 find t and c for a given smoothing factor, s.
#                             If task==1 find t and c for another value of the smoothing factor, s.
#                             There must have been a previous call with task=0 or task=1 for the same set of data
#                             (t will be stored an used internally)
#                             If task=-1 find the weighted least square spline for a given set of knots, t.
#                             These should be interior knots as knots on the ends will be added automatically.
#              s : float      A smoothing condition.
#                             The amount of smoothness is determined by satisfying the conditions:
#                                 sum((w * (y - g))**2,axis=0) <= s where g(x) is the smoothed interpolation of (x,y).
#                             The user can use s to control the tradeoff between closeness and smoothness of fit.
#                             Larger s means more smoothing while smaller values of s indicate less smoothing.
#                             Recommended values of s depend on the weights, w.
#                             If the weights represent the inverse of the standard-deviation of y, 
#                             then a good s value should be found in the range (m-sqrt(2*m),m+sqrt(2*m))
#                             where m is the number of datapoints in x, y, and w. 
#                             default : s=m-sqrt(2*m) if weights are supplied.
#                             s = 0.0 (interpolating) if no weights are supplied.
#              t : int        The knots needed for task=-1. If given then task is automatically set to -1.
#    full_output : bool       If non-zero, then return optional outputs.
#           nest : int,       optional An over-estimate of the total number of knots of the spline
#                             to help in determining the storage space. By default nest=m/2.
#                             Always large enough is nest=m+k+1           
#per : bool       If non-zero, data points are considered periodic with period x[m-1] - x[0]
#                             and a smooth periodic spline approximation is returned.
#                             Values of y[m-1] and w[m-1] are not used.
#          quiet : bool       Non-zero to suppress messages.
#Returns :	
#            tck : tuple      (t,c,k) a tuple containing the vector of knots,
#                             the B-spline coefficients, and the degree of the spline.
#              u : array      An array of the values of the parameter.
#             fp : array,     optional The weighted sum of squared residuals of the spline approximation.
#            ier : int,       optional An integer flag about splrep success. 
#                             Success is indicated if ier<=0. If ier in [1,2,3] an error occurred but was not raised.
#                             Otherwise an error is raised.
#            msg : str,       optional A message corresponding to the integer flag, ier.

class Main():
    def __init__(self):
        
        self.TStart = time.time()
        


        
        
        x = ( -77.00,  0.00, 31.00 ,45.00, 60.00, 73.00, 81.00,85.00,81.00,72.00,60.00,45.00,30.00, 0.00,-30.00,-45.00,-60.00,-72.00,-81.00,-85.00,-81.00,-73.00,-60.00,-45.00)
        y = ( -36.00,-36.00,-36.00,-36.00,-33.33,-25.75,-15.00, 0.00,15.00,25.72,33.33,36.00,36.00,36.00, 36.00, 36.00, 33.33, 25.72, 15.00,  0.00,-15.00,-25.75,-33.33,-36.00)
        z = (  30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00,30.00,30.00,30.00,30.00,30.00,30.00,30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00, 30.00)
        
        YellowPoint  = (-100.0, 50.0,70.0)
        GreenPoint   = (-100.0,-50.0,70.0)
        CyanPoint    = ( 100.0, 50.0,70.0)
        MagentaPoint = ( 100.0,-50.0,70.0)
        
        #x = (-100,-50,0,50,100)
        #y = (0,0,0,0,0)
        #z = (50,50,50,50,50)
        
        Points = (YellowPoint,GreenPoint,CyanPoint,MagentaPoint)
        
        # spline parameters
        s=0.5 # smoothness parameter
        k=3 # spline order
        nest=-1 # estimate of number of knots needed (-1 = maximal)        
        # Unverzerte Kurve
        tckp,u = splprep([x,y,z],s=s,k=k,nest=-1)
        
        
        print tckp
        
        self.Tsplprep = time.time()        
        
        tckp[1][1][2]= 0.
        tckp[1][0][5]= 0.
        tckp[1][0][6]= 0.
        tckp[1][1][10]= 0.
        #tckp[1][0][13]= 0.
        #tckp[1][1][13]= 20.
        
        maxAcc =3
        ProzentMaxAcc = 1
        ProzentMaxVel = 1
        maxVel = 5
        RParameter = 100000
        FilterVel = 1                         # Running average Vel befor diff to Acc
        GaussFilterAccGrenzParaMinima = 1           # Running Average befor Domain change
        Schiebe = 1000
        SwitchSchiebe =1

        
        (tckP1,A,ParamTime,ProzentAccGrenzParaMinima,AccGrenzParaMinima, PathLength,TotalPathTime,SumAveTime, meanVel,
         AccGrenzData, AccGrenzPara, VelTimeAccPara, VelTimeAvePara, AccData,Zeiten) = GrenzVel(tckp, Points, maxVel,ProzentMaxVel, maxAcc,ProzentMaxAcc,
                                                                           Schiebe,SwitchSchiebe,0 )


        self.TEnd = time.time()
        
        if __name__ == '__main__':
            self.Output(A,ParamTime,ProzentAccGrenzParaMinima,AccGrenzParaMinima, PathLength, TotalPathTime,SumAveTime, meanVel,
                        AccGrenzData, AccGrenzPara, VelTimeAccPara, VelTimeAvePara, AccData, maxVel, maxAcc,
                        Schiebe,SwitchSchiebe,RParameter,Zeiten)
            
    def Output(self,A,ParamTime,ProzentAccGrenzParaMinima,AccGrenzParaMinima, PathLength, TotalPathTime,SumAveTime, meanVel,
                        AccGrenzData, AccGrenzPara, VelTimeAccPara, VelTimeAvePara, AccData, maxVel, maxAcc,
                        Schiebe,SwitchSchiebe,RParameter,Zeiten):
        
        
        TStart= Zeiten[0] ; TInitPfad = Zeiten[1] ; TPathLength = Zeiten[2] ;TPathlengthByDivision = Zeiten[3];
        TReparameter = Zeiten[4]
        Tsplev = Zeiten[5]; TPos = Zeiten[6]; TVel = Zeiten[7]; TAcc = Zeiten[8]
        TFilter = Zeiten[9]; TFilter1 = Zeiten[10]; TMinimum = Zeiten[11];TDifferentiateAccGrenz = Zeiten[12];
        TSchiebe = Zeiten[13];TSpline = Zeiten[14];  TVelAccTime = Zeiten[15];TVelSplineTime = Zeiten[16]
        TAccTime = Zeiten[17];TFinish = Zeiten[18]
        print
        print 'maxVel             : %4.2f       maxAcc   :  %2.4f'%(maxVel,maxAcc)
        print        
        print 'Main Module :'
        print 'Spline preperation : %2.4f '%(self.Tsplprep-self.TStart)
        print 'Total Time         : %2.4f '%(self.TEnd- self.TStart)
        print
        print 'GrenzVel Module :'
        print 'Path init          : %2.4f     Kummuliert :  %2.4f'%(TInitPfad-TStart,                   TInitPfad-             TStart)
        print 'Path Length        : %2.4f     Kummuliert :  %2.4f'%(TPathLength-TInitPfad,              TPathLength-           TStart)
        print 'Path Len Division  : %2.4f     Kummuliert :  %2.4f'%(TPathlengthByDivision-TPathLength,  TPathlengthByDivision- TStart)
        print 'Reparameterization : %2.4f     Kummuliert :  %2.4f'%(TReparameter-TPathlengthByDivision, TReparameter-          TStart) 
        print 'Spline evaluation  : %2.4f     Kummuliert :  %2.4f'%(Tsplev-TReparameter,                Tsplev-                TStart)      
        print 'Position           : %2.4f     Kummuliert :  %2.4f'%(TPos-Tsplev,                        TPos-                  TStart)       
        print 'Vel                : %2.4f     Kummuliert :  %2.4f'%(TVel-TPos,                          TVel-                  TStart) 
        print 'Acc                : %2.4f     Kummuliert :  %2.4f'%(TAcc-TVel,                          TAcc-                  TStart)       
        print 'Parabel Steigend   : %2.4f     Kummuliert :  %2.4f'%(TFilter-TAcc,                       TFilter-               TStart)    
        print 'Parabel Fallend    : %2.4f     Kummuliert :  %2.4f'%(TFilter1-TFilter,                   TFilter1-              TStart)   
        print 'Minimum            : %2.4f     Kummuliert :  %2.4f'%(TMinimum-TFilter1,                  TMinimum-              TStart)   
        print 'Diff AccGrenz      : %2.4f     Kummuliert :  %2.4f'%(TDifferentiateAccGrenz-TMinimum,    TDifferentiateAccGrenz-TStart) 
        print 'Fenster Bildung    : %2.4f     Kummuliert :  %2.4f'%(TSchiebe-TDifferentiateAccGrenz,    TSchiebe-              TStart)
        print 'Fewnster fuellen   : %2.4f     Kummuliert :  %2.4f'%(TSpline-TSchiebe,                   TSpline-               TStart)     
        print 'Gauss              : %2.4f     Kummuliert :  %2.4f'%(TVelAccTime-TSpline,                TVelAccTime-           TStart)        
        print 'To Vel/Time Acc    : %2.4f     Kummuliert :  %2.4f'%(TVelSplineTime-TVelAccTime,         TVelSplineTime-        TStart) 
        print 'Acc                : %2.4f     Kummuliert :  %2.4f'%(TAccTime-TVelSplineTime,            TAccTime-              TStart)     
        print 'Finalize           : %2.4f     Kummuliert :  %2.4f'%(TFinish-TAccTime,                   TFinish-               TStart)         
        print  
        print 'PathLength         : %2.4f    ' %(PathLength)
        print 'Path Time          : '+str(TotalPathTime)
        print 'MeanVel            : '+str(meanVel)
        
        plt.subplot(2,1,1)
        plt.title('Max Acc : %2.2f MaxVel : %2.2f  Fenster : %i Switch : %i RParam : %i'%(maxAcc,maxVel,Schiebe,SwitchSchiebe,RParameter))        
        plt.plot(AccGrenzData[0],  AccGrenzData[1],                                              'r-',label='GrenzVel',  ms = 10.0)
        plt.plot(AccGrenzPara[0], AccGrenzPara[1],                                               'g-',label='Parabeln',  ms = 10.0)
        plt.plot(AccGrenzParaMinima[0], AccGrenzParaMinima[1],                     'r-',label='Filtered',  ms = 1.0)
        plt.plot(ProzentAccGrenzParaMinima[0], ProzentAccGrenzParaMinima[1],       'b-',label='Filtered',  ms = 1.0)
        #plt.plot(A,       'b-',label='Filtered',  ms = 1.0)
        plt.axhline()
        #plt.legend()
        plt.subplot(2,1,2)
        plt.plot(VelTimeAccPara[0]-VelTimeAccPara[0,0], VelTimeAccPara[1],          'm-',label='Vel gefeilt/Time', ms = 1.0)
        plt.plot(VelTimeAvePara[0]-VelTimeAvePara[0,0], VelTimeAvePara[1],          'c-',label='Acc gefeilt /Time', ms = 1.0)
        plt.plot(AccData[0] , AccData[1],                                           'g-',label='Acc gefeilt /Time', ms = 1.0)
        plt.plot(ParamTime[0] , ParamTime[1],                                       'b-',label='Acc gefeilt /Time', ms = 1.0)

        #plt.legend()
        plt.show()     
                  
              
               
       
if __name__ == '__main__':
    m = Main()
 
 

