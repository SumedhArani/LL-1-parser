start_state = []
terminal = []
non_terminal =[ ]
prod_rule = {}
parse_table = []

def read_file(filename):
	global start_state, prod_rule, terminal, non_terminal
	fin =open(filename)
	non_terminal=fin.readline().split()
	terminal=fin.readline().split()
	terminal.append("lambda")
	start_state=fin.readline().split()
	for state in non_terminal:
		if state not in prod_rule:
			prod_rule[state]=[]
	rule = list(map(lambda x: x[:], filter(lambda x:x!='\n', fin.readlines())))
	for x in rule:
		temp = list(map(str.strip, x.split("->")))
		prod_rule[temp[0]] = prod_rule[temp[0]]+[z.strip() for z in temp[1].split("|")]

def parts(x):
	components = []
	i, j = 0, 0
	while i<len(x):
		if x[i:j+1] in terminal or x[i:j+1] in non_terminal:
			components.append(x[i:j+1])
			i=j+1
		j+=1
	return components

def first(x):
	first_set =set()
	components = parts(x)
	i=0
	#if non terminal at the beginning
	if components[i] in terminal:
		first_set.add(components[i])
	elif components[i]=='lambda':
		first_set.add(components[i])
	else:
		for each_rule in prod_rule[components[i]]:
			first_set= first_set | first(each_rule)
		if 'lambda' in first_set:
			while 'lambda' in first_set and i<len(components)-1:
				first_set.remove('lambda')
				i+=1
				if components[i] in terminal:
					first_set.add(components[i])
				elif components[i]=='lambda':
					first_set.add(components[i])
				else:
					for each_rule in prod_rule[components[i]]:
						first_set= first_set | first(each_rule)
			first_set.add('lambda')
	return first_set

def follow(symbol):
	follow_set = set()
	if symbol in start_state:
		follow_set.add('$')
	sym_prods = [(nt, rule)for nt in prod_rule for rule in prod_rule[nt] if symbol in parts(rule)]
	for nt, rule in sym_prods:
		beta = rule.split(symbol,1)[1]
		if beta!='':
			follow_set = follow_set | first(beta)
		print(follow_set)
		if 'lambda' in follow_set or beta=='':
			if 'lambda' in follow_set:
				follow_set.remove('lambda')
			if nt!=symbol:
				follow_set = follow_set | follow(nt)
				pass
	return follow_set

def fill_table():
	pass

def parse():
	pass

def main():
	read_file("input.txt")
	print(first("S"))
	
if __name__ == '__main__':
	main()
