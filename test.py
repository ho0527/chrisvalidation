from validation import *

data={
	"name": 123
}
rule={
	"name": "nullable|string"
}
error={
	"string": ":key必須是字串"
}
print(validate(data,rule,error))