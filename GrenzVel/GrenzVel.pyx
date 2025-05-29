#!python
##cython: boundscheck=False


import numpy as np
cimport numpy as np
from scipy.ndimage.filters import gaussian_filter as gf
from scipy.interpolate import  splev, splrep
from scipy.integrate import romberg
from libc.math cimport sqrt

import time
    # tckp                      + tckp from splprep
    # Points                    + Coordinates of Yellow, Green,Cyan,Magenta 
    # maxVel                    + max Vel
    # maxAcc                    + max Acc
    # RParameter                + Interpolation density for reparametrization
    # LA                        + Length of running Average Velocity
    # Schiebe                   + Width of Maximum Window
    # LA4                       + Decay of GaussFilter for AccGrenz Para Minima
    # SwitchSchiebe             + Incremental windob building or one shot

def GrenzVel(tckp,Points,double maxVel,double ProzentMaxVel, double maxAcc, double ProzentMaxAcc, int Schiebe, int SwitchSchiebe,int debug):


    #cdef double TStart = time.time()
    
    ProzentMaxVel = max(min(ProzentMaxVel,1),0.1)
    ProzentMaxAcc = max(min(ProzentMaxAcc,1),0.1)
    
    cdef int RParameter = 100000
    
    cdef int Density = 100
    cdef double DDensity = 100.0
    cdef size_t i
    cdef size_t j
    
    cdef double YPx = Points[0][0]
    cdef double YPy = Points[0][1]
    cdef double YPz = Points[0][2]
    cdef double GPx = Points[1][0]
    cdef double GPy = Points[1][1]
    cdef double GPz = Points[1][2]
    cdef double CPx = Points[2][0]
    cdef double CPy = Points[2][1]
    cdef double CPz = Points[2][2]
    cdef double MPx = Points[3][0]
    cdef double MPy = Points[3][1]
    cdef double MPz = Points[3][2]

    cdef np.ndarray[np.double_t, ndim=1] YellowPoint 
    cdef np.ndarray[np.double_t, ndim=1] GreenPoint  
    cdef np.ndarray[np.double_t, ndim=1] CyanPoint   
    cdef np.ndarray[np.double_t, ndim=1] MagentaPoint
    
  
    YellowPoint  = np.array([YPx,YPy,YPz])
    GreenPoint   = np.array([GPx,GPy,GPz])
    CyanPoint    = np.array([CPx,CPy,CPz])
    MagentaPoint = np.array([MPx,MPy,MPz])
    
    
    cdef np.ndarray[np.double_t, ndim=1] ParamIn
    ParamIn = np.linspace(0,1,RParameter)
    
    cdef np.ndarray[np.double_t, ndim=1] W   
    W = np.linspace(0,1,RParameter)
    
    cdef np.ndarray[np.double_t, ndim=1] SegmentPunkteX
    cdef np.ndarray[np.double_t, ndim=1] SegmentPunkteY
    cdef np.ndarray[np.double_t, ndim=1] SegmentPunkteZ
    
    SegmentPunkteX,SegmentPunkteY,SegmentPunkteZ = splev(W,tckp)
    
    cdef np.ndarray[np.double_t, ndim=1] SumLengthU    
    SumLengthU = np.zeros(RParameter,dtype = np.double)
    for i in range(1, RParameter):
        SumLengthU[i]= SumLengthU[i-1]+ sqrt((SegmentPunkteX[i]-SegmentPunkteX[i-1])**2+
                                             (SegmentPunkteY[i]-SegmentPunkteY[i-1])**2+
                                             (SegmentPunkteZ[i]-SegmentPunkteZ[i-1])**2)
    
    cdef double PathLength = SumLengthU[RParameter-1]

       
    #cdef double  TInitPfad = time.time()
    #cdef double TPathlength = time.time()
    #cdef double TPathlengthByDivision = time.time()
    
 
    tckP1 = splrep(SumLengthU, ParamIn, w=None, xb=None, xe=None, k=3, task=0, s=0, t=None,full_output=0, per=0, quiet =1) 
    

   
    cdef int Teilung = int(PathLength*Density)+1
    cdef np.ndarray[np.double_t, ndim=1] PosIntervalle
    PosIntervalle = np.linspace(0,PathLength,Teilung)
    
    cdef np.ndarray[np.double_t, ndim=1] Param
    Param = splev(PosIntervalle, tckP1)    
    
    #cdef double TReparameter = time.time()
    
    cdef np.ndarray[np.double_t, ndim=1] PathPosX 
    cdef np.ndarray[np.double_t, ndim=1] PathPosY
    cdef np.ndarray[np.double_t, ndim=1] PathPosZ
    
    PathPosX,PathPosY,PathPosZ = splev(Param,tckp)
    
    
    #cdef double Tsplev = time.time()
    
    # Positions 
    cdef np.ndarray[np.double_t, ndim=2] YellowPosData
    cdef np.ndarray[np.double_t, ndim=2] GreenPosData
    cdef np.ndarray[np.double_t, ndim=2] CyanPosData
    cdef np.ndarray[np.double_t, ndim=2] MagentaPosData
    
    YellowPosData   = np.zeros((2,Teilung),dtype = np.double)
    GreenPosData    = np.zeros((2,Teilung),dtype = np.double)
    CyanPosData     = np.zeros((2,Teilung),dtype = np.double)
    MagentaPosData  = np.zeros((2,Teilung),dtype = np.double)
    
    for i in range(0, Teilung):
            YellowPosData[0,i] = i/DDensity 
            YellowPosData[1,i] = sqrt((PathPosX[i]   - YellowPoint[0])**2+
                                     (PathPosY[i]   - YellowPoint[1])**2+
                                     (PathPosZ[i]   - YellowPoint[2])**2)
            
            GreenPosData[0,i] = i/DDensity
            GreenPosData[1,i] = sqrt((PathPosX[i]   - GreenPoint[0])**2+
                                    (PathPosY[i]   - GreenPoint[1])**2+
                                    (PathPosZ[i]   - GreenPoint[2])**2)
            
            CyanPosData[0,i] = i/DDensity
            CyanPosData[1,i] = sqrt((PathPosX[i]   - CyanPoint[0])**2+
                                   (PathPosY[i]   - CyanPoint[1])**2+
                                   (PathPosZ[i]   - CyanPoint[2])**2)
            MagentaPosData[0,i] = i/DDensity
            MagentaPosData[1,i] = sqrt((PathPosX[i]   - MagentaPoint[0])**2+
                                      (PathPosY[i]   - MagentaPoint[1])**2+
                                      (PathPosZ[i]   - MagentaPoint[2])**2)

    #print 'PosData'
    #print YellowPosData
    #print YellowPosData.shape[1]    

    #cdef double TPos = time.time()
    
    #------------------------------------------------------------------------------------------- Positions

    # Velocities
    cdef np.ndarray[np.double_t, ndim=2] YellowVelData   
    cdef np.ndarray[np.double_t, ndim=2] GreenVelData    
    cdef np.ndarray[np.double_t, ndim=2] CyanVelData     
    cdef np.ndarray[np.double_t, ndim=2] MagentaVelData  
    YellowVelData    = np.zeros((2,Teilung-1),dtype = np.double)
    GreenVelData     = np.zeros((2,Teilung-1),dtype = np.double)
    CyanVelData      = np.zeros((2,Teilung-1),dtype = np.double)
    MagentaVelData   = np.zeros((2,Teilung-1),dtype = np.double)

    cdef double vY
    cdef double vG
    cdef double vC
    cdef double vM
    cdef double vYg
    cdef double vGg
    cdef double vCg
    cdef double vMg
    cdef double vg
    for i in range(0,Teilung-1):
            vY  = ((YellowPosData[1,i+1]-YellowPosData[1,i])*Density)          
            YellowVelData[0,i] = i/DDensity
            YellowVelData[1,i] = vY
            vG = ((GreenPosData[1,i+1]-GreenPosData[1,i])*Density)
            GreenVelData[0,i]  = i/DDensity
            GreenVelData[1,i]  = vG
            vC = ((CyanPosData[1,i+1]-CyanPosData[1,i])*Density)
            CyanVelData[0,i]   = i/DDensity
            CyanVelData[1,i]   = vC
            vM = ((MagentaPosData[1,i+1]-MagentaPosData[1,i])*Density) 
            MagentaVelData[0,i] = i/DDensity
            MagentaVelData[1,i] = vM
            
    #print 'VelData'
    #print YellowVelData
    #print YellowVelData.shape[1]
    
    #cdef double TVel = time.time()
    
    
    #------------------------------------------------------------------------------------------- Velocities
    
   
    #cdef double TVelAverage = time.time()
    
    #------------------------------------------------------------------------------------------- Filtered Velocities

    #Accelerations from VelDataAverage
    cdef np.ndarray[np.double_t, ndim=1] AccIntervalle
    AccIntervalle = np.linspace(0,PathLength,Teilung-2)
    
    cdef double deltaX = YellowVelData[0,0]-YellowVelData[0,1]
    
    cdef np.ndarray[np.double_t, ndim=2] YellowAccData   
    cdef np.ndarray[np.double_t, ndim=2] GreenAccData    
    cdef np.ndarray[np.double_t, ndim=2] CyanAccData     
    cdef np.ndarray[np.double_t, ndim=2] MagentaAccData 
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzData   
    
    YellowAccData         = np.zeros((2,Teilung-2),dtype = np.double)
    GreenAccData          = np.zeros((2,Teilung-2),dtype = np.double)
    CyanAccData           = np.zeros((2,Teilung-2),dtype = np.double)
    MagentaAccData        = np.zeros((2,Teilung-2),dtype = np.double)
    AccGrenzData          = np.zeros((2,Teilung-2),dtype = np.double)
    
    cdef double aY
    cdef double aG
    cdef double aC
    cdef double aM     
    cdef double aYg
    cdef double aGg
    cdef double aCg
    cdef double aMg
    
    for i in range(0,Teilung-2):   
        #aY = ((YellowVelDataAverage[1,i+1]-YellowVelDataAverage[1,i])/deltaX)
        if (YellowVelData[0,i+1]-YellowVelData[0,i]) == 0.0:
            aY = 100.0
        else:
            aY = ((YellowVelData[1,i+1]-YellowVelData[1,i])/
                  (YellowVelData[0,i+1]-YellowVelData[0,i]))
        YellowAccData[0,i]  = AccIntervalle[i]
        YellowAccData[1,i]  = aY
        #aG = ((GreenVelDataAverage[1,i+1]-GreenVelDataAverage[1,i])/deltaX)
        if (GreenVelData[0,i+1]-GreenVelData[0,i]) == 0.0:
            aG = 100.0
        else:
            aG = ((GreenVelData[1,i+1]-GreenVelData[1,i])/
                  (GreenVelData[0,i+1]-GreenVelData[0,i]))
        GreenAccData[0,i]   = AccIntervalle[i]
        GreenAccData[1,i]   = aG
        #aC = ((CyanVelDataAverage[1,i+1]-CyanVelDataAverage[1,i])/deltaX)
        if (CyanVelData[0,i+1]-CyanVelData[0,i]) == 0.0:
            aC = 100.0
        else:
            aC = ((CyanVelData[1,i+1]-CyanVelData[1,i])/
                  (CyanVelData[0,i+1]-CyanVelData[0,i]))
        CyanAccData[0,i]    = AccIntervalle[i]
        CyanAccData[1,i]    = aC
        #aM = ((MagentaVelDataAverage[1,i+1]-MagentaVelDataAverage[1,i])/deltaX)
        if (MagentaVelData[0,i+1]-MagentaVelData[0,i]) == 0.0:
            aM = 100.0
        else:
            aM = ((MagentaVelData[1,i+1]-MagentaVelData[1,i])/
                  (MagentaVelData[0,i+1]-MagentaVelData[0,i]))
        MagentaAccData[0,1] = AccIntervalle[i]
        MagentaAccData[1,i] = aM 
        
        aYg= min(sqrt(1/abs(aY)),maxVel)
        aGg= min(sqrt(1/abs(aG)),maxVel)
        aCg= min(sqrt(1/abs(aC)),maxVel)
        aMg= min(sqrt(1/abs(aM)),maxVel)
        
        aG = min(aYg,aGg,aCg,aMg)
        AccGrenzData[0,i]  = AccIntervalle[i]
        AccGrenzData[1,i]  = aG
    
    #print 'AccGrenzData'
    #print AccGrenzData
    #print AccGrenzData.shape[1]
    
    AccGrenzData[0,0]  = 0.0
    AccGrenzData[1,0]  = 0.001
    AccGrenzData[1,-1] = 0.001
        
    #cdef double TAcc = time.time()
    
    #------------------------------------------------------------------------------------------- AccGrenzData
    
    # steigende Parabeln 
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzDataFilter 
    AccGrenzDataFilter=np.zeros((2,Teilung-2-1),dtype = np.double) 
    cdef double Intervall = 1.0/(AccGrenzData[0,1]-AccGrenzData[0,0])         
    #cdef int Flag0 = 0
    cdef int Flag0 = 1
    cdef int l = 0
    for i in range(0,Teilung-2-1):
        if ((AccGrenzData[1,i+1]-AccGrenzData[1,i])/
            (AccGrenzData[0,i+1]-AccGrenzData[0,i]) > maxAcc/AccGrenzData[1,i]) and Flag0 ==0:
            Flag0 = 1
            if l == 0 :
                l = i
            AccGrenzDataFilter[0,i] = AccGrenzData[0,i]
            AccGrenzDataFilter[1,i] = ParaUp(AccGrenzData[0,l],AccGrenzData[1,l],maxAcc,i,Intervall)
        else:
            if Flag0 ==1:
                AccGrenzDataFilter[0,i] = AccGrenzData[0,i]
                AccGrenzDataFilter[1,i] = ParaUp(AccGrenzData[0,l],AccGrenzData[1,l],maxAcc,i,Intervall)
                if AccGrenzDataFilter[1,i] > AccGrenzData[1,i]:
                    Flag0 = 0 ; l = 0
            else:
                AccGrenzDataFilter[0,i] = AccGrenzData[0,i]
                AccGrenzDataFilter[1,i] = AccGrenzData[1,i]
                l = 0 
                
    #print 'Steigende Parabeln'
    #print AccGrenzDataFilter
    #print AccGrenzDataFilter.shape[1]
    
    #cdef double TFilter = time.time()

    
    # fallende Parabeln 
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzDataFilter1
    AccGrenzDataFilter1=np.zeros((2,Teilung-2),dtype = np.double)         
    #Flag0 = 0
    Flag0 = 1
    l = Teilung-2-1
    for i in range(Teilung-2-1,0,-1):

        if ((AccGrenzData[1,i-1]-AccGrenzData[1,i])/
            (AccGrenzData[0,i-1]-AccGrenzData[0,i]) <- maxAcc/AccGrenzData[1,i]) and Flag0 ==0:
            Flag0 = 1
            if l == 0 :
                l = i
                AccGrenzDataFilter1[0,i] = AccGrenzData[0,i]
                AccGrenzDataFilter1[1,i] = ParaDown(AccGrenzData[0,l],AccGrenzData[1,l],maxAcc,i,Intervall)
        else:
            if Flag0 ==1:
                AccGrenzDataFilter1[0,i] = AccGrenzData[0,i]
                AccGrenzDataFilter1[1,i] = ParaDown(AccGrenzData[0,l],AccGrenzData[1,l],maxAcc,i,Intervall)
                if AccGrenzDataFilter1[1,i] > AccGrenzData[1,i]:
                    Flag0 = 0; l = 0
            else: 
                AccGrenzDataFilter1[0,i] = AccGrenzData[0,i]
                AccGrenzDataFilter1[1,i] = AccGrenzData[1,i]
                l = 0
    AccGrenzDataFilter1[1,-1]=0.01
    
    #print 'Fallende Parabeln'
    #print AccGrenzDataFilter1
    #print AccGrenzDataFilter1.shape[1]
    
    #cdef double TFilter1 = time.time()

 
    # Minimum finden
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzPara
    AccGrenzPara  =np.zeros((2,Teilung-2),dtype = np.double)
    for i in range(0,Teilung-2-1):
        AccGrenzPara[0,i] = AccGrenzDataFilter1[0,i]
        AccGrenzPara[1,i] = min(AccGrenzDataFilter1[1,i],AccGrenzDataFilter[1,i])
        
    AccGrenzPara[0,-1] = PathLength
    
    #print 'Minimum'
    #print AccGrenzData
    #print AccGrenzData.shape[1]
    
    #cdef double TMinimum = time.time()
    
    #---------------------------------------------------------------------------------------- AccGrenzPara 

   
    #################### Differentiate AccGrenzPara
    cdef np.ndarray[np.double_t, ndim=2] AccAccGrenzPara
    AccAccGrenzPara  =np.zeros((2,Teilung-2-1),dtype = np.double)
    for i in range(0,Teilung-2-1):
        AccAcc = (AccGrenzPara[1,i+1]-AccGrenzPara[1,i])/(AccGrenzPara[0,i+1]-AccGrenzPara[0,i])
        AccAccGrenzPara[0,i]= AccGrenzPara[0,i]
        AccAccGrenzPara[1,i]= AccAcc #max(min(AccAcc,4),-4)
    AccAccGrenzPara[1,-1] = AccAccGrenzPara[1,-2]            
        
    #print 'AccAcc'
    #print AccAccGrenzPara
    #print AccAccGrenzPara.shape[1]
    
    #cdef double TDiferentiateAccGrenz = time.time()
   
    #---------------------------------------------------------------------------------------- IntGrenzPara
    ######################################################################################### create find Maxima and create Window of Zeros
    cdef np.ndarray[np.double_t, ndim=1] AccGrenzParaRR = np.zeros((Teilung-2-1),dtype = np.double)   #AccGrenzPara.shape[1]
    cdef np.ndarray[np.double_t, ndim=1] AccGrenzParaRL = np.zeros((Teilung-2-1),dtype = np.double) #AccGrenzPara.shape[1]
    cdef np.ndarray[np.double_t, ndim=1] Zeros          = np.zeros(AccGrenzPara.shape[1],dtype = np.double)
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzParaM  = np.copy(AccGrenzPara)
    if SwitchSchiebe == 1 :
        for i in range (1,int(Schiebe/10)):        
            AccGrenzParaRR   = np.roll(AccGrenzPara[1],i*10)        
            AccGrenzParaRL   = np.roll(AccGrenzPara[1],(Teilung-2-1)-i*10) 
            AccGrenzParaM    = np.vstack((AccGrenzPara[0],np.where(((AccGrenzPara[1] >= AccGrenzParaRR) & (AccGrenzPara[1] >= AccGrenzParaRL)),Zeros,AccGrenzParaM[1])))
    else:
        AccGrenzParaRR       = np.roll(AccGrenzPara[1],Schiebe)        
        AccGrenzParaRL       = np.roll(AccGrenzPara[1],-Schiebe) 
        AccGrenzParaM = np.vstack((AccGrenzPara[0],np.where(((AccGrenzPara[1] >= AccGrenzParaRR[1]) & (AccGrenzPara[1] >= AccGrenzParaRL[1])),Zeros,AccGrenzParaM[1])))
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzParaZeros
    AccGrenzParaZeros = np.copy(AccGrenzParaM)
    
    #print 'AccGrenzParaM'
    #print AccGrenzParaM
    #print AccGrenzParaM.shape[1] 

    #cdef double TSchiebe = time.time()
    
    cdef size_t n
    cdef double APointX 
    cdef double APointY 
    cdef double A1PointX
    cdef double A1PointY
    cdef double BPointX 
    cdef double BPointY 
    cdef double B1PointX
    cdef double B1PointY    
    j = 0
    cdef double m
    cdef double p
    for i in range(2,(Teilung-2-1-1)):
        if AccGrenzParaM[1,i]== 0:
            APointX = AccGrenzParaM[0,i-1]
            APointY = AccGrenzParaM[1,i-1]
            A1PointX = AccGrenzParaM[0,i-2]
            A1PointY = AccGrenzParaM[1,i-2]
            while (AccGrenzParaM[1,i+j]== 0.0):
                j=j+1
        BPointX = AccGrenzParaM[0,i+j]
        BPointY = AccGrenzParaM[1,i+j]
        B1PointX = AccGrenzParaM[0,i+j+1]
        B1PointY = AccGrenzParaM[1,i+j+1]
        #for n in range(0,j):
            #y = calcParabel(APointX,APointY,A1PointX,A1PointY,BPointX,BPointY,B1PointX,B1PointY, AccGrenzParaM[0,i+n])
            #AccGrenzParaM[1,i+n] = y
        for n in range(1,j+1):
            if j-1 == 0:
                p = 0
            else:
                m = <double>j-1
                p = (n-1)/m
            #x =EvaluateSplineX(APointX,APointY,A1PointX,A1PointY,BPointX,BPointY,B1PointX,B1PointY, p)
            y =EvaluateSplineY(APointX,APointY,A1PointX,A1PointY,BPointX,BPointY,B1PointX,B1PointY, p)
            #AccGrenzParaM[0,i+n-1] = x
            AccGrenzParaM[1,i+n-1] = y
        j=0
    
    #print 'AccGrenzParaMinima'
    #print AccGrenzParaMinima
    #print AccGrenzParaMinima.shape[1]
    
    # Minimum finden
    
    #cdef double TSpline =  time.time()
    
    cdef np.ndarray[np.double_t, ndim=2] AccGrenzParaMinima
    AccGrenzParaMinima  =np.zeros((2,Teilung-2-1-1),dtype = np.double)
    for i in range(0,Teilung-2-1-1):
        AccGrenzParaMinima[0,i] = AccGrenzParaM[0,i]
        AccGrenzParaMinima[1,i] = min(AccGrenzPara[1,i],AccGrenzParaM[1,i])
    
    #cdef double TGauss = time.time()
    
    # Prozentsatz anwenden
    cdef np.ndarray[np.double_t, ndim=2] ProzentAccGrenzParaMinima
    ProzentAccGrenzParaMinima  =np.zeros((2,Teilung-2-1-1),dtype = np.double)
    for i in range(0,Teilung-2-1-1):
        ProzentAccGrenzParaMinima[0,i] = AccGrenzParaMinima[0,i]
        ProzentAccGrenzParaMinima[1,i] = ProzentMaxVel * AccGrenzParaMinima[1,i]
    
    ########################################################################################################
    ######################################################################################### Domain Wechsel
    ########################################################################################################
    
    ########### VelTime Para  aus AccGrenzPara
    
    cdef double Time    = 0.0
    cdef double SumTime = 0.0 
    
    cdef np.ndarray[np.double_t, ndim=2] VelTimeAccPara
    VelTimeAccPara   =np.zeros((2,Teilung-2),dtype = np.double)
    for i in range(0,Teilung-2-1):    
        Time = (AccGrenzPara[0,i+1]-AccGrenzPara[0,i])/((AccGrenzPara[1,i+1]+AccGrenzPara[1,i])/2)
        SumTime = SumTime+Time
        VelTimeAccPara[0,i]= SumTime
        VelTimeAccPara[1,i]=AccGrenzPara[1,i]
    VelTimeAccPara[0,-1] = SumTime+Time
    VelTimeAccPara[1,-1] = 0.0
    
    #print 'AccGrenzParaMinimaAverage'
    #print AccGrenzParaMinimaAverage
    #print AccGrenzParaMinimaAverage.shape[1]
    
    #cdef double TVelTime = time.time()
    
    
    
    ########### Vergleich mit gemitteltem AccGrenzParaMinimaAverage 
    
    SumTime = 0.0
    cdef np.ndarray[np.double_t, ndim=2] VelTimeAvePara = np.zeros((2,(Teilung-2-1-1)),dtype = np.double)

    for i in range(1,(Teilung-2-1-1)-1):        
        Time = (ProzentAccGrenzParaMinima[0,i+1]-ProzentAccGrenzParaMinima[0,i])/((ProzentAccGrenzParaMinima[1,i+1]+ProzentAccGrenzParaMinima[1,i])/2)
        SumTime = SumTime+Time
        VelTimeAvePara[0,i]  = SumTime
        VelTimeAvePara[1,i]  = ProzentAccGrenzParaMinima[1,i]    
    VelTimeAvePara[0,-1] = SumTime+Time
    VelTimeAvePara[1,-1] = 0.0
    
    #cdef double Parameter    = 0.0
    #cdef double SumParameter = 0.0
    #cdef np.ndarray[np.double_t, ndim=2] ParamTime =np.zeros((2,(Teilung-2-1-1-1)),dtype = np.double)
    
    #for i in range(0,(Teilung-2-1-1)-1):
        #Parameter     = (VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i])*((VelTimeAvePara[1,i+1]+VelTimeAvePara[1,i])/2)
        #SumParameter = SumParameter + Parameter
        #ParamTime[0,i] = VelTimeAvePara[0,i]
        #ParamTime[1,i] = SumParameter

    
    
    #print 'VelTimeAvePara'
    #print VelTimeAvePara
    #print VelTimeAvePara.shape[1]
    
    #cdef double TVelGaussTime = time.time()
    
    ######### Differentiate CutVelTimeIntGrenzParaAverage
    
    cdef np.ndarray[np.double_t, ndim=2] AccData
    AccData  =np.zeros((2,VelTimeAvePara.shape[1]-1),dtype = np.double)
    for i in range(0,VelTimeAvePara.shape[1]-1):
        if (VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i]) == 0.0:
            aY = 100.0
        else:
            aY = ((VelTimeAvePara[1,i+1]-VelTimeAvePara[1,i])/(VelTimeAvePara[0,i+1]-VelTimeAvePara[0,i]))
        AccData[0,i]  = VelTimeAvePara[0,i]-VelTimeAvePara[0,0]
        AccData[1,i]  = aY
    AccData[1,0] = AccData[1,1]
    AccData[1,-1] = AccData[1,-2]
    
    #cdef np.ndarray[np.double_t, ndim=2] AccAccData
    #AccAccData  =np.zeros((2,AccData.shape[1]-1),dtype = np.double)
    #for i in range(0,AccData.shape[1]-1):   
        #aY = ((AccData[1,i+1]-AccData[1,i])/(AccData[0,i+1]-AccData[0,i]))
        #AccAccData[0,i]  = VelTimeAvePara[0,i]-VelTimeAvePara[0,0]
        #AccAccData[1,i]  = aY
    #AccAccData[1,0] = AccAccData[1,1]
    #AccAccData[1,-1] = AccAccData[1,-2]
    
    #print 'AccData'
    #print AccData
    #print AccData.shape[1]
    
    #cdef double TAccTime = time.time()


    cdef double SumAccTime = VelTimeAccPara[0,-1]-VelTimeAccPara[0,0]
    cdef double SumAveTime = VelTimeAvePara[0,-1]-VelTimeAvePara[0,0]
    cdef double MeanVel       = PathLength/SumAccTime
    cdef double TotalPathAccTime = SumAccTime
    
    #cdef double TFinish = time.time()
    
    #Zeiten = (TStart,TInitPfad,TPathlength,TPathlengthByDivision,TReparameter,Tsplev,TPos,TVel,TVelAverage,
              #TAcc,TFilter,TFilter1,TMinimum,TDiferentiateAccGrenz,TSchiebe,
              #TSpline,TGauss,TVelTime,TVelGaussTime,TAccTime,TFinish)
              
    if debug == 1:
        import matplotlib.pyplot as plt
        plt.subplot(2,1,1)
        plt.title('Max Acc : %2.2f MaxVel : %2.2f Fenster : %i Switch : %i RParam : %i'%(maxAcc,maxVel,Schiebe,SwitchSchiebe,RParameter))        
        plt.plot(AccGrenzData[0],  AccGrenzData[1],                                'r-',label='GrenzVel',  ms = 10.0)
        plt.plot(AccGrenzPara[0], AccGrenzPara[1],                                 'g-',label='Parabeln',  ms = 10.0)
        plt.plot(AccGrenzParaMinima[0], AccGrenzParaMinima[1],       'r-',label='Filtered',  ms = 1.0)
        plt.axhline()
        #plt.legend()
        plt.subplot(2,1,2)
        plt.plot(VelTimeAccPara[0]-VelTimeAccPara[0,0], VelTimeAccPara[1],          'm-',label='Vel gefeilt/Time', ms = 1.0)
        plt.plot(VelTimeAvePara[0]-VelTimeAvePara[0,0], VelTimeAvePara[1],          'c-',label='Acc gefeilt /Time', ms = 1.0)
        plt.plot(AccData[0] , AccData[1],                                           'g-',label='Acc gefeilt /Time', ms = 1.0) 
        #plt.legend()
        plt.show() 
        

    return (tckP1,SumLengthU,ProzentAccGrenzParaMinima,AccGrenzParaMinima,
            PathLength, TotalPathAccTime, SumAveTime, MeanVel,
            AccGrenzData , AccGrenzPara, VelTimeAccPara , VelTimeAvePara, AccData)
            
        
            
    # Pathlength                   + Pathlength
    # TotalPathTime                + Total Path Time
    # MeanVel                      + Average Velocity
    # AccGrenzData                 + Raw max Velocities along Path so that Acc of winches does not excede Limit
    # AccGrenzPara                 + Max Velocities so that we dont excede winch limits while traveling along Path
    # AccGrenzParaMinimaAverage    + rounded Acc Grenz Para peaks removed Main Output in Path domain
    # VelTimeAccPara               + Vel over Time from AccGrenzPara (max Vel reachable)
    # VelTimeAvePara               + Vel over Time from AccGrenzParaMinimaAverage
    # AccData                      + Acc over Time from VelTimeAvePara

    


cdef double ParaUp(double Px,double Py,double a,int i,double Intervall):        
    x=Px;  y=Py
    if abs(y) < 0.01:
        c= 2*a; b = x
    else:
        c = 2*a ; b = x- y**2/(2*a)
    return sqrt(abs((i-(b*(Intervall)))*c/Intervall))
    
cdef double ParaDown(double Px,double Py,double a,int i,double Intervall):         
    x=Px ;  y=Py;
    if abs(y) < 0.01 :
        c = -2*a; b = x
    else:
        c = -2*a ; b = x-y**2/(2*-a)
    return sqrt(abs(((b*(Intervall)-i))*c/Intervall))
    
    
cdef double EvaluateSplineY(double x1, double y1,
                            double x11,double y11,
                            double x2, double y2,
                            double x12,double y12,
                            double p):
                           
    cdef double k1 = (y11-y1)/(x11-x1)
    cdef double k2 = (y12-y2)/(x12-x2)                      
    
    cdef double  t1 = -((-k2*x1 + k2*x2 + y1 - y2)/(k1 - k2))
    cdef double  t2 = -(x1 - x2 - (-k2*x1 + k2*x2 + y1 - y2)/(k1 - k2))

    cdef double y = (2*p**3-3*p**2+1)*y1+(p**3-2*p**2+p)*(t1*k1)+(-2*p**3+3*p**2)*y2+(p**3-p**2)*(t2*k2)

    return y