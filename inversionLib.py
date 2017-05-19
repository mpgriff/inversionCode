import numpy as np

def simulated_annealing(func, mo, bound, T, b):
	"""simulated annealing algorithm to optimize a function
		#----------inputs-------------#
		func: the function to be minimized (accepts a model m)
		mo:   the initial guess model (numpy 1XM)
		bounds: boundaries for the model parameters (numpy array [Mx2])
		T: acceptance parametrization array (numpy array)
		b: number of repeated perturbations per temperature step (integer)

		#----------outputs------------#
		mlist, Elist

		mlist: a list with all the tested models
		Elist: a list of the objective function values evaluated for each test model"""
	npar = len(mo)
	
	Elist = [func(mo)]
	mlist = [mo]

	for j, tt in enumerate(T):
		for h in range(0, b):
			# Go through and perturb each parameter at the given T.
			for k in range(0, npar):
				dm = np.random.normal(0., abs(bound[k][1]-bound[k][0])/20.)
				mnew = mlist[-1]*1.
				mnew[k] = mlist[-1][k] + dm

				#check to make sure perturbation is within bounds. rejects MH criteria.
				if( (mnew[k] > bound[k][1]) or (mnew[k] < bound[k][0])):
					Elist.append(Elist[-1])
					mlist.append(mlist[-1])
				else:
					#get energy for perturbed model.

					En = func(mnew)
					deltaE = En-Elist[-1]
					#if new energy is lower accept perturbation.
					if(deltaE <= 0): 
						Elist.append(En)
						mlist.append(mnew)

					#challenge new perturbed model with a random number.
					else:

						Godzilla = np.random.uniform(0., 1.)
						MonsterZero = np.exp(-1.*deltaE/tt)

						if(Godzilla <= MonsterZero):
							Elist.append(En)
							mlist.append(mnew)
						else:
							Elist.append(Elist[-1])
							mlist.append(mlist[-1])
		print '\rSA -I{0}{1}I-'.format('|'*((j+1)*50/len(T)), ' '*(50 - (j+1)*50/len(T))),

	return mlist, Elist
