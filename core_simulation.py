import time
import queue
import threading

from Functions import *
import os

def Polydisperce_star(N_average,k,number_arms,target_dir,t_production=10**5,replicas=200, a=1,update_callback=None):
    """
    Your actual simulation function.

    parameter a is for the subset of linear chains 
    """
    folder=f"\\f={number_arms}_k={k}"

    if not os.path.exists(target_dir+folder):
        os.mkdir(target_dir+folder)
    for i in range(replicas):
        if update_callback:
            # Send: ("Progress", stage_name, stage_percent, current_replica_index)
            update_callback("Relaxation", 0, i)
        if k==None:
            arms=N_average*np.ones(number_arms,dtype=int)
        else:
            arms=Zimm_Schultz(N_average,k,number_arms)
        
        Initial=Polymer_adsorb_initiator(arms, a)
        try: type(Initial)==tuple
        except: print( "too many arms")
        Cx,Cy,Cz=Initial
        # --- 1. RELAXATION STAGE ---
        # Put your real relaxation loop here
        for step in range(20*sum(arms)):
            Cx,Cy,Cz=Star_pivot(arms,Cx,Cy,Cz)
            # Periodically calculate percent and notify UI if callback exists
            if update_callback and step % 5 == 0:
                percent = int((step /(20*sum(arms))) * 100)
                update_callback("Relaxation", percent,i)
        if update_callback:
            # We pass a copy of the dictionary values so they don't change mid-render
            coords = (Cx.copy(),Cy.copy(),Cz.copy())
            update_callback("Plot", coords,i)
        #plot_3d_walk(Cx,Cy,Cz)
        traj=np.vstack((np.hstack(tuple(Cx.values())),np.hstack(tuple(Cy.values())),np.hstack(tuple(Cz.values())))).T
        np.savetxt(target_dir+folder+"\\Star_init_"+str(arms)+".txt",traj)
        RG=open(target_dir+folder+"\\Star_RG_"+str(arms)+".txt","w")
        AD=open(target_dir+folder+"\\Star_AD_"+str(arms)+".txt","w")
        SD=open(target_dir+folder+"\\Star_SD_"+str(arms)+".txt","w")

        # --- 2. PRODUCTION STAGE ---
        # Put your real production/pivot loops here
        for step in range(t_production):
            Cx,Cy,Cz=Star_pivot(arms,Cx,Cy,Cz)
            traj=np.vstack((np.hstack(tuple(Cx.values())),np.hstack(tuple(Cy.values())),np.hstack(tuple(Cz.values())))).T
            rg,Ad,Sd=param_calc(traj)
            RG.write(str(rg)+"\n")
            AD.write(str(Ad)+"\n")
            SD.write(str(Sd)+"\n")
            
            if update_callback and step % 20 == 0:
                percent = int((step / t_production) * 100)
                update_callback("Production", percent,i)
        RG.close()
        AD.close()
        SD.close()




def LAMMPS_setup(architecture,N_average,k,number_arms,target_dir,a=1,concentration=None,update_callback=None):
    if architecture == "Linear":
        if k==None:
            arms=N_average*np.ones(number_arms,dtype=int)
        else:
            arms=Zimm_Schultz(N_average,k,number_arms)
            
        Initial=Polymer_adsorb_initiator(arms, a)
        try: type(Initial)==tuple
        except: print( "too many arms")
        Cx,Cy,Cz=Initial
        for step in range(20*sum(arms)):
            Cx,Cy,Cz=Star_pivot(arms,Cx,Cy,Cz)
            if update_callback and step % 5 == 0:
                percent = int((step /(20*sum(arms))) * 100)
                update_callback("Relaxation", percent,step)
    
        traj=np.vstack((np.hstack(tuple(Cx.values())),np.hstack(tuple(Cy.values())),np.hstack(tuple(Cz.values())))).T
        box=Rg_chain_prediction(N_average*number_arms)+20
        BOX=(2*box)**3
        rng = np.random.default_rng()
        particles=[]
        if concentration!=None:
            n=0
            while n<int(concentration*BOX):
                random_ints = rng.integers(low=-box, high=box, size=3)
                PP=np.array(particles)
                test=[int(sum(i==random_ints)) for i in traj]
                test2=[int(sum(i==random_ints)) for i in PP]
                if 3 not in test:
                    if 3 not in test2:
                        particles.append(random_ints)
                        n=n+1
        atom_type=1 if concentration==None else 2
        file=open(target_dir+"\\NN_adsorb.txt","w")
        file.write("LAMMPS data file from restart file: timestep = 0.\n\n")
        file.write(str(len(particles)+traj.shape[0])+" atoms\n")
        file.write(str(traj.shape[0]-number_arms)+" bonds\n")
        file.write((f"0 angles\n0 dihedrals\n0 impropers\n\n{atom_type} atom types\n1 bond types\n0 angle types\n"+
        "0 dihedral types\n0 improper types\n0 extra bond per atom\n"+
        "-"+str(box+2)+" "+str(box+2)+" xlo xhi\n-"+str(box+2)+" "+str(box+2)+" ylo yhi\n-"+str(box+2)+" "+str(box+2)+" zlo zhi\n"))
        if concentration==None:
            file.write("\nMasses\n\n1 1\n")
        else:
            file.write("\nMasses\n\n1 1\n")
            file.write("2 1\n\n")
        file.write("Atoms\n\n")
    
        for i in range(1,number_arms+1):
            for j in range(1,arms[i-1]+1):
                file.write(str((i-1)*arms[i-1]+j)+" "+str(i)+" 1 "+str(traj[(i-1)*arms[i-1]+j-1])[1:-1]+"\n")
        if concentration!=None:
            for i in range(len(particles)):
                file.write(str(traj.shape[0]+1+i)+" "+str(number_arms+1)+" 2 "+str(particles[i])[1:-1]+"\n")
        file.write("\nVelocities\n\n")
        for i in range(len(particles)+traj.shape[0]):
            file.write(str(i+1)+" 0 0 0\n")
        file.write("\nBonds\n\n")
        for i in range(1,number_arms+1):
            for j in range(1,arms[i-1]):
                file.write(str((i-1)*(arms[i-1]-1)+j)+" 1 "+str((i-1)*arms[i-1]+j)+" "+str((i-1)*arms[i-1]+j+1)+"\n")
        file.close()
    elif architecture == "Star":
        if k==None:
            arms=N_average*np.ones(number_arms,dtype=int)
        else:
            arms=Zimm_Schultz(N_average,k,number_arms)
            
        Initial=Polymer_adsorb_initiator(arms, a)
        try: type(Initial)==tuple
        except: print( "too many arms")
        Cx,Cy,Cz=Initial
        # --- 1. RELAXATION STAGE ---
        # Put your real relaxation loop here
        for step in range(20*sum(arms)):
            Cx,Cy,Cz=Star_pivot(arms,Cx,Cy,Cz)
            # Periodically calculate percent and notify UI if callback exists
            if update_callback and step % 5 == 0:
                percent = int((step /(20*sum(arms))) * 100)
                update_callback("Relaxation", percent,step)
        #plot_3d_walk(Cx,Cy,Cz)
        traj=np.vstack((np.hstack(tuple(Cx.values())),np.hstack(tuple(Cy.values())),np.hstack(tuple(Cz.values())))).T
        box=Rg_chain_prediction(N_average*number_arms)+20
        BOX=(2*box)**3
        rng = np.random.default_rng()
        particles=[]
        if concentration!=None:
            n=0
            while n<int(concentration*BOX):
                random_ints = rng.integers(low=-box, high=box, size=3)
                PP=np.array(particles)
                test=[int(sum(i==random_ints)) for i in traj]
                test2=[int(sum(i==random_ints)) for i in PP]
                if 3 not in test:
                    if 3 not in test2:
                        particles.append(random_ints)
                        n=n+1
        atom_type=1 if concentration==None else 2
        core=np.array([0,0,0])
        def Reading(TJ,core):
            ## x= atoms in all previous stars
            Atoms=[]
            for i in TJ: 
                if all(i==core): continue
                else: 
                    Atoms.append(i)
            Bonds=[[1,2]]
            Atoms=np.array(Atoms)
            for i in range(len(Atoms)-1):
                if np.sum((Atoms[:-1]-Atoms[1:])**2,axis=1)[i]==1:
                    Bonds.append([i+2,i+3])
                else:
                    Bonds.append([1,i+3])
            return (Atoms,Bonds)
        Atoms=[]
        Bonds=[]
        Atoms.append(np.hstack((np.array([1,1,1]),core)).astype(int))
        A,B=Reading(traj,core)
        for i in range(len(A)):
            Atoms.append(np.hstack((np.array([i+2,1,1]),A[i])).astype(int))
        for i in range(len(B)):
            Bonds.append(np.hstack((np.array([1+i,1]),B[i])).astype(int))

        file=open(target_dir+"\\NN_star.txt","w")
        print(target_dir+"NN_star.txt")
        file.write("LAMMPS data file from restart file: timestep = 0.\n\n")
        file.write(str(len(Atoms)+len(particles))+" atoms\n")
        file.write(str(len(Bonds))+" bonds\n")
        file.write((f"0 angles\n0 dihedrals\n0 impropers\n\n{atom_type} atom types\n1 bond types\n0 angle types\n"+
        "0 dihedral types\n0 improper types\n0 extra bond per atom\n"+
        "-"+str(box)+" "+str(box)+" xlo xhi\n-"+str(box)+" "+str(box)+" ylo yhi\n-"+str(box)+" "+str(box)+" zlo zhi\n"))

        if concentration==None:
            file.write("\nMasses\n\n1 1\n")
        else:
            file.write("\nMasses\n\n1 1\n")
            file.write("2 1\n\n")
        file.write("Atoms\n\n")

        for i in range(len(Atoms)):
            file.write(str(Atoms[i])[1:-1]+"\n")
        for i in range(len(particles)):
            file.write(str(traj.shape[0]+2+i)+" "+str(number_arms+1)+" 2 "+str(particles[i])[1:-1]+"\n")
        file.write("\nVelocities\n\n")
        for i in range(len(particles)+len(Atoms)):
            file.write(str(i+1)+" 0 0 0\n")
        file.write("\nBonds\n\n")
        for i in range(len(Bonds)):
            file.write(str(Bonds[i])[1:-1]+"\n")
        file.close()
    else:
        pass
