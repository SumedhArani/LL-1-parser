start_state = []
terminal = []
non_terminal =[ ]
prod_rule = {}
parse_table = []
visited = []
parse_table = {}
f_visited = []

def read_file(filename):
	global start_state, prod_rule, terminal, non_terminal
	fin =open(filename)
	non_terminal = fin.readline().split()
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
	while j<len(x):
		if x[i:j+1] in terminal or x[i:j+1] in non_terminal:
			components.append(x[i:j+1])
			i=j+1
		j+=1
	return components

def first(x):
	#wrapper function
	global visited
	visited.clear()
	first_set = find_first(x)
	return first_set

def find_first(x):
	global visited
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
			if each_rule not in visited:
				visited.append(each_rule)
				first_set= first_set | find_first(each_rule)
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
						if each_rule not in visited:
							visited.append(each_rule)
						first_set= first_set | find_first(each_rule)
			first_set.add('lambda')
	return first_set

def follow(symbol):
	#wrapper function
	global f_visited
	f_visited.clear()
	follow_set = find_follow(symbol)
	return follow_set

def find_follow(symbol):
	global f_visited
	follow_set = set()
	if symbol in start_state:
		follow_set.add('$')
	sym_prods = [(nt, rule)for nt in prod_rule for rule in prod_rule[nt] if symbol in parts(rule)]
	for nt, rule in sym_prods:
		beta = rule.split(symbol,1)[1]
		if beta!='':
			follow_set = follow_set | first(beta)
		if 'lambda' in follow_set or beta=='':
			if 'lambda' in follow_set:
				follow_set.remove('lambda')
			if nt!=symbol and rule not in f_visited:
				f_visited.append(rule)
				follow_set = follow_set | find_follow(nt)
				
	return follow_set

def fill_table():
	global parse_table
	col_heads = [x for x in terminal]
	col_heads.remove('lambda')
	col_heads.append('$')
	for nt in non_terminal:
		if nt not in parse_table:
			parse_table[nt] ={}
			for ch in col_heads:
				if ch not in parse_table[nt]:
					parse_table[nt][ch] = ""
	for nt in prod_rule:
		for each_rule in prod_rule[nt]:
			first_set = first(each_rule)
			if 'lambda' not in first_set:
				for t in first_set:
					if parse_table[nt][t] == '':
						parse_table[nt][t] = each_rule
					else:
						print("Given grammar is not LL(1)")
						return False
			else:
				follow_set = follow(nt)
				for t in follow_set:
					if parse_table[nt][t] == '':
						parse_table[nt][t] = each_rule
					else:
						print("Given grammar is not LL(1)")
						return False
	return True

def parse(w):
	inp_stack = [l for l in w]+['$']
	sym_stack = start_state+['$']
	while sym_stack[0] != '$':
		if inp_stack[0] == sym_stack[0]:
			inp_stack.pop(0)
			sym_stack.pop(0)
		elif sym_stack[0] == 'lambda': 
			sym_stack.pop(0)
		elif sym_stack[0] not in non_terminal: 
			return False
		else:
			new = [x for x in parts(parse_table[sym_stack[0]][inp_stack[0]])]
			if new == []: 
				return False
			else:
				sym_stack.pop(0)
				sym_stack = new + sym_stack
	if sym_stack[0] == inp_stack[0]: 
		return True
	else: 
		return False
	
def main():
	read_file("input.txt")
	print(first("A"));
	if fill_table():
		w = input("Enter string to be parsed('exit' to end): ")
		while w!='exit':
			result = parse(w)
			print(result)
			w = input("Enter string to be parsed('exit' to end): ")

if __name__ == '__main__':
	main()
