# define pso function

def pso(costfunction,nvar,varmax,varmin,maxiter,nPop,constri_coeff):
    
    # nPop: Population Size (Swarm Size)
    
    # nvar: Number of Decision Variables (search space)
    # each decision variable is the each particle's location
    # type : tuple
    varsize=(1,nvar)
    
    if constri_coeff:
        #Constriction Coefficients
        phi1=2.05
        phi2=2.05
        phi=phi1+phi2
        chi=2/(phi-2+np.sqrt(phi**2-4*phi))
        w=chi         
        wdamp=1       
        c1=chi*phi1   
        c2=chi*phi2   
    else:
        w=1            # Inertia Weight
        wdamp=0.99     # Inertia Weight Damping Ratio
        c1=1.5         # Personal Learning Coefficient
        c2=2.0         # Global Learning Coefficient
    
    # Velocity Limits
    VelMax=0.1*(varmax-varmin)
    VelMin= -VelMax
    
    # Initialization
    empty_particle={}
    best={}
    
    # only one! 沒有每一個particle都有，整體只有一個
    # set initial global best to infinite
    Globalbest={'gcost':np.inf,'gposition':None}
    
    Position=[]
    cost=[]
    velocity=[]
    particle=[]
    best.update({'Position':Position,'cost':cost})
    
    empty_particle.update({'Position':[],'cost':[],'velocity':[],'best':best})
    
    print('empty particle\n: %s'%particle)
    
    #initialize population's position , velocity , evaluation
    
    for i in range(nPop):
        
        particle.append(empty_particle.copy())
        
        # initialize position
        particle[i]['Position']= np.random.uniform(varmin,varmax,size=varsize)       
        
        # initialize velocity
        particle[i]['velocity']=np.zeros(varsize)
        
        # evaluation
        particle[i]['cost']= costfunction(particle[i]['Position'])
        
        # update personal best
        particle[i]['best']['Position']= particle[i]['Position'].copy()
        particle[i]['best']['cost']=particle[i]['cost'].copy()
        
        # update global best
        if (particle[i]['best']['cost']) <Globalbest['gcost']:
            Globalbest['gcost'] = (particle[i]['best']['cost'].copy())
            Globalbest['gposition'] = (particle[i]['best']['Position'].copy())

        print(particle[i])
        print('\n')
        
    print('After initialization:\n%s'%particle)

    bestcost=[]
    
    for it in range(maxiter):
        
        for i in range(0, nPop):
            
            ## update velocity
            
            particle[i]['velocity'] = w*particle[i]['velocity'] +\
                        c1*np.random.random(varsize)*(particle[i]['best']['Position']-particle[i]['Position'])+\
                        c2*np.random.random(varsize)*(Globalbest['gposition']-particle[i]['Position'])
            
            # Apply Velocity Limits
            particle[i]['velocity']=np.maximum(particle[i]['velocity'],VelMin)
            particle[i]['velocity']=np.minimum(particle[i]['velocity'],VelMax)
            
            # Update Position
            
            particle[i]['Position'] += particle[i]['velocity']
            
            # Evaluation
            
            particle[i]['cost'] = costfunction(particle[i]['Position'])
            
            # Update Personal Best
            
            #print('cost:%s'%particle[i]['cost'])
            #print('total cost:%s'%particle[i]['best']['cost'])
            
            if  particle[i]['cost'] < particle[i]['best']['cost']:
                
                print('Personal cost:%s'%particle[i]['cost']+', Global best cost:%s'%particle[i]['best']['cost'])
                
                particle[i]['best']['Position'] = particle[i]['Position'].copy()
                particle[i]['best']['cost'] = particle[i]['cost'].copy()
                
                # Update Global Best
                
                if particle[i]['best']['cost'].sum()<Globalbest['gcost']:
                    
                    Globalbest['gcost']=particle[i]['best']['cost'].copy()
                    Globalbest['gposition']=particle[i]['best']['Position'].copy()
        
        print('\n %s'%particle)
        bestcost.append(Globalbest)
        
        w=w*wdamp
    
    return print('\n global best cost :\n %s '%Globalbest['gcost']+',\n\n global best location :\n %s'%Globalbest['gposition']+',\n\n bestcost :\n %s'%bestcost)