from random import randint,choice

lower_case = "abcdefghijklmnopqrstuvwxyz"
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "!#$%&/()=[+*]^|-_:;{}.,<>?¿¡'\"\\"


def pass_gen(lower: bool,upper: bool,number: bool,symbol: bool,long: int):
	if long > 1000:
		return "Why would you need a password that long?"
	if long == 0:
		return "Password length cannot be equal to the amount of bitches you got"
	if long < 0:
		return "!browssaq htgnel evitagen a evah t'nac uoy tud yrt eciN"
	options = {}
	password = ""
	options.update({lower_case:lower})
	options.update({upper_case:upper})
	options.update({numbers:number})
	options.update({symbols:symbol})
	for value in list(options):
		if not options.get(value):
			del options[value]
	if options == {}:
		return "At least one parameter must be True"
	for i in range(long):
		element = choice(list(options))
		password += element[randint(0,len(element)-1)]
	return password