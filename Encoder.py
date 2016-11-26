from GroundedLiteral import *

def getFunctionNameTerms(f_string):
	i_first=f_string.index("(")
	i_last=f_string.index(")")
	name=f_string[0:i_first]
	terms=f_string[i_first+1:i_last]
	term=terms.strip(" ").split(',')
	return [name,term]

def templateNameCreator(f_name,n_terms):
	template_name=f_name+"("

	for i in range(1,n_terms):
		if i!=n_terms:
			template_name+="$x"+str(i)+"$,"
		else:
			template_name+="$x"+str(i)+"$)"
	return template_name
def groundedLiteralNameGenerator(f_name,terms):
	name=f_name + "("

	for i in range(0,len(terms)):
		if i!=len(terms)-1:
			name+=terms[i]+","
		else:
			name+=terms[i]+")"
	return name
class Encoder(object):
	"""docstring for Encoder"""



	def __init__(self,argv):
		#Lists of initial and goal literals
		self.init_lit=[]
		self.goal_lit=[]
		self.terms_list=[]

		f=open(argv[1],'r')
		for line in f:
			words=line.strip("\n").split()

			if line[0]=='I':
				for arg in words[1:]:
					name,terms = getFunctionNameTerms(arg)
					
					#USE name and terms list here
					for t in terms:
						if not (t in self.terms_list):
							self.terms_list.append(t)

					if name[0]=="-":
						signal=False
						name=name[1:]
					else:
						signal=True
					ident = groundedLiteralNameGenerator(name,terms)
					print(ident)
					g_lit = GroundedLiteral(ident,signal)
					self.init_lit.append

			if line[0]=='A':
				
				action_part = line[1:].strip(" ").split(":")[0]
				i_colon=line.index(":")
				i_arrow=line.index(">")
				precond_part = line[i_colon+1:i_arrow-1].strip("\n").split(" ")	
				effect_part=line[i_arrow+1:].strip("\n").split(" ")

				action_name,action_terms = getFunctionNameTerms(action_part)
				print(action_name,action_terms)
				#USE ACTION name and terms list here
				for arg in precond_part:
					if arg!="":
						precond_name,precond_terms = getFunctionNameTerms(arg)
						print(precond_name,precond_terms)
				for arg in effect_part:
					if arg!="":
						effect_name,effect_terms = getFunctionNameTerms(arg)
						print(effect_name,effect_terms)

			if line[0]=='G':
				for arg in words[1:]:
					name,terms = getFunctionNameTerms(arg)		
					#USE name and terms list here
					for t in terms:
						if not (t in self.terms_list):
							self.terms_list.append(t)

					if name[0]=="-":
						signal=False
						name=name[1:]
					else:
						signal=True
					ident = groundedLiteralNameGenerator(name,terms)
					print(ident)
					g_lit = GroundedLiteral(ident,signal)
					self.goal_lit.append


	def generateSentence(self):
		pass


					

