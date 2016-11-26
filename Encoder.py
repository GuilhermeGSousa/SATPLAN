from GroundedLiteral import *

def getFunctionNameTerms(f_string):
	i_first=f_string.index("(")
	i_last=f_string.index(")")
	name=f_string[0:i_first]
	terms=f_string[i_first+1:i_last]
	term=terms.strip(" ").split(',')
	return [name,term]

def templateNameCreator(f_name,terms):
	template_name=f_name+"("
	for i in range(0,len(terms)):
		if i!=len(terms)-1:
			if not terms[i][0].isupper():
				template_name+="$"+terms[i]+"$,"
			else:
				template_name+=terms[i]+","
		else:
			if not terms[i][0].isupper():
				template_name+="$"+terms[i]+"$)"
			else:
				template_name+=terms[i]+")"
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
		#Lists of initial and goal literals (GROUNDED)
		self.init=[]
		self.goals=[]
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
					g_lit = GroundedLiteral(ident,signal)
					self.init.append(g_lit)

			if line[0]=='A':
				
				action_part = line[1:].strip(" ").split(":")[0]
				i_colon=line.index(":")
				i_arrow=line.index(">")
				precond_part = line[i_colon+1:i_arrow-1].strip("\n").split(" ")	
				effect_part=line[i_arrow+1:].strip("\n").split(" ")

				action_name,action_terms = getFunctionNameTerms(action_part)
				print(templateNameCreator(action_name,action_terms))
				#USE ACTION name and terms list here
				for arg in precond_part:
					if arg!="":
						precond_name,precond_terms = getFunctionNameTerms(arg)
						print(templateNameCreator(precond_name,precond_terms))
				for arg in effect_part:
					if arg!="":
						effect_name,effect_terms = getFunctionNameTerms(arg)
						print(templateNameCreator(effect_name,effect_terms))

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
					
					g_lit = GroundedLiteral(ident,signal)
					self.goals.append(g_lit)



	def generateSentence(self):
		pass


					

