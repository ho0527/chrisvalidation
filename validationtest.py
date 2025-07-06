import unittest
from validation import *

class TestValidation(unittest.TestCase):
	def test001validdata(self):
		result=validate({
			"username":"admin",
			"password":"123456"
		},{
			"username":"required|string",
			"password":["required","string","min:5"]
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error",
			"min":"ERROR_datatype_error"
		})
		self.assertTrue(result["success"])
		self.assertEqual(result["data"],{
			"username":"admin",
			"password":"123456"
		})
		self.assertIsNone(result["error"])

	def test002invalidusernametype(self):
		result=validate({
			"username":123,
			"password":"123456"
		},{
			"username":"required|string",
			"password":["required","string","min:5"]
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error",
			"min":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"string":"ERROR_datatype_error"
			}
		})
		self.assertEqual(result["error"],"ERROR_datatype_error")

	def test003missingusername(self):
		result=validate({
			"password":"123456"
		},{
			"username":"required|string",
			"password":["required","string","min:5"]
		},{
			"username.required":"user name required.",
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error",
			"min":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required":"user name required."
			}
		})
		self.assertEqual(result["error"],"user name required.")

	def test004shortpasswordandmissingusername(self):
		result=validate({
			"password":"1234"
		},{
			"username":"required|string",
			"password":["required","string","min:5"]
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error",
			"min":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required":"The 'username' field is required."
			},
			"password":{
				"min":"ERROR_datatype_error"
			}
		})
		self.assertEqual(result["error"],"The 'username' field is required.")

	def test005checkalltrue(self):
		result=validate({
			"password":"123"
		},{
			"username":"required|string",
			"password":["required","string","min:5"]
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error",
			"min":"ERROR_datatype_error"
		},True)
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required":"The 'username' field is required."
			},
			"password":{
				"min":"ERROR_datatype_error"
			}
		})
		self.assertEqual(result["error"],"The 'username' field is required.")

	def test006nestedarray(self):
		result=validate({
			"users":[
				{"email":"abc@example.com"},
				{"email":"123"},
				{"name":"no email"}
			]
		},{
			"users.*.email":"required|string|min:5"
		},{
			"required":":key 為必填欄位",
			"string":":key 必須是文字格式",
			"min":":key 長度不足"
		},True)
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"users.1.email":{
				"min":"'email' 長度不足"
			},
			"users.2.email":{
				"required":"'email' 為必填欄位"
			}
		})

	def test007validemail(self):
		result=validate({
			"email":"user@example.com"
		},{
			"email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertTrue(result["success"])
		self.assertEqual(result["data"],{
			"email":"user@example.com"
		})
		self.assertIsNone(result["error"])

	def test008invalidemail(self):
		result=validate({
			"email":"invalid-email"
		},{
			"email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"email":{
				"email":"The 'email' must be a valid email."
			}
		})
		self.assertEqual(result["error"],"The 'email' must be a valid email.")

	def test009emptyemail(self):
		result=validate({
			"email":""
		},{
			"email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"email":{
				"required":"The 'email' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'email' field is required.")

	def test010emailnone(self):
		result=validate({
			"email":None
		},{
			"email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"email":{
				"required":"The 'email' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'email' field is required.")

	def test011emailmissing(self):
		result=validate({
			"username":"aaa"
		},{
			"email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"email":{
				"required":"The 'email' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'email' field is required.")

	def test012emptyusername(self):
		result=validate({
			"username":""
		},{
			"username":"required|string"
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required": "The 'username' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'username' field is required.")

	def test013usernameisnone(self):
		result=validate({
			"username":None
		},{
			"username":"required|string"
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required":"The 'username' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'username' field is required.")

	def test014usernamemissing(self):
		result=validate({
			"email":"abc@example.com"
		},{
			"username":"required|string"
		},{
			"required":"The :key field is required.",
			"string":"ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"username":{
				"required":"The 'username' field is required."
			}
		})
		self.assertEqual(result["error"],"The 'username' field is required.")

	def test015invalidnestedobject(self):
		result=validate({
			"user":{
				"email":"invalid"
			}
		},{
			"user.email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"user.email":{
				"email":"The 'email' must be a valid email."
			}
		})
		self.assertEqual(result["error"],"The 'email' must be a valid email.")

	def test016validnestedobject(self):
		result=validate({
			"user":{
				"email":"valid@example.com"
			}
		},{
			"user.email":"required|email"
		},{
			"required":"The :key field is required.",
			"email":"The :key must be a valid email."
		})
		self.assertTrue(result["success"])
		self.assertEqual(result["data"],{
			"user":{
				"email":"valid@example.com"
			}
		})
		self.assertIsNone(result["error"])

	def test017validateinteger(self):
		result=validate({
			"age":20
		},{
			"age":"required|integer"
		},{
			"required":"The :key field is required.",
			"integer":"The :key must be an integer."
		})
		self.assertTrue(result["success"])
		self.assertEqual(result["data"],{
			"age":20
		})
		self.assertIsNone(result["error"])

	def test018validateinvalidinteger(self):
		result=validate({
			"age":"twenty"
		},{
			"age":"required|integer"
		},{
			"required":"The :key field is required.",
			"integer":"The :key must be an integer."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"age":{
				"integer":"The 'age' must be an integer."
			}
		})
		self.assertEqual(result["error"],"The 'age' must be an integer.")

	def test019checkbooleanfield(self):
		result=validate({
			"is_active":True
		},{
			"is_active":"required|boolean"
		},{
			"required":"The :key field is required.",
			"boolean":"The :key must be true or false."
		})
		self.assertTrue(result["success"])
		self.assertEqual(result["data"],{
			"is_active":True
		})
		self.assertIsNone(result["error"])

	def test020checkinvalidbooleanfield(self):
		result=validate({
			"is_active":"word"
		},{
			"is_active":"required|boolean"
		},{
			"required":"The :key field is required.",
			"boolean":"The :key must be true or false."
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"is_active":{
				"boolean":"The 'is_active' must be true or false."
			}
		})
		self.assertEqual(result["error"],"The 'is_active' must be true or false.")

	def test021errorvalue(self):
		result=validate({
			"test": "1231223"
		},{
			"test": "required|min:min"
		},{
			"required": "The :key field is required.",
			"min": "ERROR_datatype_error"
		})
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"test":{
				"min":"ERROR_datatype_error"
			}
		})
		self.assertEqual(result["error"],"ERROR_datatype_error")

	def test022manynest(self):
		result=validate({
			"nest1":[
				{
					"nest2": {
						"nest3": [
							{
								"nest4": {
									"key": 123
								}
							},{
								"nest4": {
									"key": "string"
								}
							},{
								"nest4": {}
							}
						]
					}
				}
			]
		},{
			"nest1.*.nest2.nest3.*.nest4.key": "required|string"
		},{
			"required": "ERROR_request_data_not_found",
			"string": "ERROR_datatype_error"
		},True)
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"nest1.0.nest2.nest3.0.nest4.key":{
				"string": "ERROR_datatype_error"
			},
			"nest1.0.nest2.nest3.2.nest4.key":{
				"required": "ERROR_request_data_not_found"
			}
		})
		self.assertEqual(result["error"],"ERROR_datatype_error")

	def test023nullablerequiredfail(self):
		data={
			"name": None
		}
		rule={
			"name": "required"
		}
		error={
			"required": ":key為必填"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])
		self.assertEqual(result["error"], "'name'為必填")

	def test024nullablepass(self):
		data={
			"name": None
		}
		rule={
			"name": "nullable|string"
		}
		error={
			"string": ":key必須是字串"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])
		self.assertIsNone(result["error"])

	def test025nullablestringfail(self):
		data={
			"name": 123
		}
		rule={
			"name": "nullable|string"
		}
		error={
			"string": ":key必須是字串"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])
		self.assertEqual(result["error"], "'name'必須是字串")

	def test026arraysuccess(self):
		data={
			"name": []
		}
		rule={
			"name": "array"
		}
		error={
			"string": ":key必須是字串"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test027jsonsuccess(self):
		data={
			"name": {
				"test": "abc"
			}
		}
		rule={
			"name": "required|json"
		}
		error={
			"json": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test028regexsuccess(self):
		data={
			"name": "abc"
		}
		rule={
			"name": "required|regex:/^[a-z]+$/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test029regexsuccess(self):
		data={
			"name": "abc123"
		}
		rule={
			"name": "required|regex:/^[a-z]+/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test030regexsuccess(self):
		data={
			"name": "123abc"
		}
		rule={
			"name": "required|regex:/[a-z]+$/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test031regexsuccess(self):
		data={
			"name": "123abc321"
		}
		rule={
			"name": "required|regex:/[a-z]+/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test032regexerror(self):
		data={
			"name": "123abc"
		}
		rule={
			"name": "required|regex:/^[a-z]+$/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])

	def test033regexerror(self):
		data={
			"name": "123abc123"
		}
		rule={
			"name": "required|regex:/[a-z]+$/"
		}
		error={
			"regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])

	def test034notregexsuccess(self):
		data={
			"name": "123abc123"
		}
		rule={
			"name": "required|not_regex:/^[0-9]+$/"
		}
		error={
			"not_regex": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test035acceptedsuccess(self):
		data={
			"name": "1"
		}
		rule={
			"name": "required|accepted"
		}
		error={
			"accepted": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test036acceptedsuccess2(self):
		data={
			"name": True
		}
		rule={
			"name": "required|accepted"
		}
		error={
			"accepted": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test037acceptederror(self):
		data={
			"name": "false"
		}
		rule={
			"name": "required|accepted"
		}
		error={
			"accepted": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])

	def test039acceptedifsuccess(self):
		data={
			"agree": "yes",
			"type": "confirm"
		}
		rule={
			"agree": "accepted_if:type,confirm"
		}
		error={
			"accepted_if": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertTrue(result["success"])

	def test040acceptediferror(self):
		data={
			"agree": "no",
			"type": "confirm"
		}
		rule={
			"agree": "accepted_if:type,confirm"
		}
		error={
			"accepted_if": "ERROR_request_datatype_error"
		}
		result=validate(data,rule,error)
		self.assertFalse(result["success"])

	def test041bailsuccess(self):
		result=validate({
			"key": "abc"
		},{
			"key": "bail|required|string|min:2"
		},{
			"bail": "ERROR_bail",
			"required": "ERROR_required",
			"string": "ERROR_type_string",
			"min": "ERROR_min_length"
		},True)
		self.assertTrue(result["success"])

	def test042bailfail(self):
		result=validate({
			"key": 123
		},{
			"key": "bail|required|string|min:2"
		},{
			"bail": "ERROR_bail",
			"required": "ERROR_required",
			"string": "ERROR_type_string",
			"min": "ERROR_min_length"
		},True)
		self.assertFalse(result["success"])
		self.assertEqual(result["data"],{
			"key": {
				"string": "ERROR_type_string"
			}
		})
		self.assertEqual(result["error"],"ERROR_type_string")
if __name__=="__main__":
	unittest.main()