import ipaddress
import re
import socket

customrules={}  # 自訂驗證規則儲存區
null=[None,"",[],{}]

def registerrule(name,func):
	customrules[name]=func  # 註冊自訂驗證規則

def validate(data,rule,error,checkall=False):
	check=True  # 整體驗證結果
	errordata={}  # 所有錯誤訊息
	firsterror=None  # 第一個錯誤訊息（給 error 欄位用）

	# 建立錯誤資訊
	def seterror(testkey,rulename):
		return {
			"check": False,
			"rulename": rulename,
			"errordata": error.get(testkey+"."+rulename,error.get(rulename))
		}

	# 取得數值的長度或數值本身（依類型）
	def checksize(value):
		if isinstance(value,str) or isinstance(value,list):
			return len(value)
		if isinstance(value,int) or isinstance(value,float):
			return value
		if isinstance(value,dict) and "size" in value:
			return value["size"]
		return False

	# 根據點路徑取得巢狀資料
	def getvaluebypath(data,path):
		keys=path.split(".")
		for key in keys:
			if isinstance(data,list):
				try:
					key=int(key)
				except:
					return None
			if isinstance(data,dict) and key in data:
				data=data[key]
			elif isinstance(data,list) and isinstance(key,int) and 0<=key<len(data):
				data=data[key]
			else:
				return None
		return data

	# 將 key 中含 * 的欄位展開為實際所有符合的欄位
	def expandwildcardkeys(data,path):
		parts=path.split(".")
		results=[""]
		for part in parts:
			if part=="*":
				temp=[]
				for r in results:
					d=getvaluebypath(data,r[1:] if r.startswith(".") else r)
					if isinstance(d,list):
						for i in range(len(d)):
							temp.append(r+"."+str(i))
				results=temp
			else:
				results=[r+"."+part for r in results]
		return [r[1:] if r.startswith(".") else r for r in results]

	# 執行單一欄位規則驗證
	def test(testkey,testrule,value):
		testrule=testrule.split(":")
		rulename=testrule[0]
		rulevalue=testrule[1] if 1<len(testrule) else ""
		rulevaluelist=rulevalue.split(",") if rulevalue else []

		# 必填判斷
		if rulename=="required":
			if value in null:
				return seterror(testkey,rulename)

		# nullable 已在外層處理，這邊不處理

		if value is not None:
			if False:
				# 預留給 future 的處理
				if not customrules[rulename](value,rulevaluelist):
					return seterror(testkey,rulename)
			elif rulename=="accepted":
				if value not in ["yes","on",1,"1",True,"true"]:
					return seterror(testkey,rulename)
			elif rulename=="accepted_if":
				if len(rulevaluelist)!=2:
					return seterror(testkey,rulename)
				otherkey=rulevaluelist[0]
				othervalue=rulevaluelist[1]
				othertarget=getvaluebypath(data,otherkey)
				if othertarget==othervalue:
					if value not in ["yes","on",1,"1",True,"true"]:
						return seterror(testkey,rulename)
			elif rulename=="active_url":
				try:
					host=re.sub(r"^https?://","",value).split("/")[0]
					socket.gethostbyname(host)
				except:
					return seterror(testkey,rulename)
			elif rulename=="array":
				if not isinstance(value,list):
					return seterror(testkey,rulename)
			elif rulename in ["boolean","bool"]:
				if not isinstance(value,bool) and value not in [0,1,"0","1"]:
					return seterror(testkey,rulename)
			elif rulename=="email":
				if type(value)!=str or not re.match(r"^[^@]+@[^@]+\.[^@]+$",value):
					return seterror(testkey,rulename)
			elif rulename=="in":
				allowed=rulevaluelist
				if isinstance(value,list):
					for key in value:
						if str(key) not in allowed:
							return seterror(testkey,rulename)
				else:
					if str(value) not in allowed:
						return seterror(testkey,rulename)
			elif rulename in ["integer","int"]:
				if not isinstance(value,int) and not isinstance(value,float):
					return seterror(testkey,rulename)
			elif rulename=="ip":
				try:
					ipaddress.ip_address(value)
				except:
					return seterror(testkey,rulename)
			elif rulename=="ipv4":
				try:
					if not isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address):
						return seterror(testkey,rulename)
				except:
					return seterror(testkey,rulename)
			elif rulename=="ipv6":
				try:
					if not isinstance(ipaddress.ip_address(value), ipaddress.IPv6Address):
						return seterror(testkey,rulename)
				except:
					return seterror(testkey,rulename)
			elif rulename in ["json","object","dictionary","dict"]:
				if not isinstance(value,dict):
					return seterror(testkey,rulename)
			elif rulename=="max":
				try:
					size=checksize(value)
					if size==False or int(rulevaluelist[0])<size:
						return seterror(testkey,rulename)
				except:
					return seterror(testkey,rulename)
			elif rulename=="min":
				try:
					size=checksize(value)
					if size==False or size<int(rulevaluelist[0]):
						return seterror(testkey,rulename)
				except:
					return seterror(testkey,rulename)
			elif rulename=="not_regex":
				if type(value)!=str:
					return seterror(testkey,rulename)

				pattern=rulevalue

				if pattern.startswith("/") and pattern.rfind("/")>0:
					lastslash=pattern.rfind("/")
					regexbody=pattern[1:lastslash]
					flags=pattern[lastslash+1:]
					flagval=0
					if "i" in flags:
						flagval|=re.IGNORECASE
					if "m" in flags:
						flagval|=re.MULTILINE
					if "s" in flags:
						flagval|=re.DOTALL
					pattern=regexbody
				else:
					flagval=0

				try:
					regex=re.compile(pattern,flagval)
				except:
					return seterror(testkey,rulename)

				if regex.search(value):
					return seterror(testkey,rulename)
			elif rulename=="regex":
				if type(value)!=str:
					return seterror(testkey,rulename)

				pattern=rulevalue

				if pattern.startswith("/") and pattern.rfind("/")>0:
					lastslash=pattern.rfind("/")
					regexbody=pattern[1:lastslash]
					flags=pattern[lastslash+1:]
					flagval=0
					if "i" in flags:
						flagval|=re.IGNORECASE
					if "m" in flags:
						flagval|=re.MULTILINE
					if "s" in flags:
						flagval|=re.DOTALL
					pattern=regexbody
				else:
					flagval=0

				try:
					regex=re.compile(pattern,flagval)
				except:
					return seterror(testkey,rulename)

				if not regex.search(value):
					return seterror(testkey,rulename)
			elif rulename in ["string","str"]:
				if not isinstance(value,str):
					return seterror(testkey,rulename)
			elif rulename=="size":
				size=checksize(value)
				if size==False or size!=int(rulevaluelist[0]):
					return seterror(testkey,rulename)
			elif rulename in ["bail","required", "nullable"]:
				pass  # 已經處理過
			elif rulename in customrules:
				if not customrules[rulename](value,rulevaluelist):
					return seterror(testkey,rulename)
			else:
				return seterror(testkey,rulename)

		return {
			"check": True,
			"rulename": rulename,
			"errordata": None
		}

	# 依據每個規則欄位進行驗證
	for key in rule:
		testrulelist=rule[key]
		if isinstance(testrulelist,str):
			testrulelist=testrulelist.split("|")

		expanded_keys=expandwildcardkeys(data,key)

		for fullkey in expanded_keys:
			value=getvaluebypath(data,fullkey)

			# nullable 欄位值為空，直接跳過所有驗證
			if not (("nullable" in testrulelist) and (value==None)):
				bailstop=False
				for testrule in testrulelist:
					if bailstop:
						break
					returndata=test(fullkey,testrule,value)

					if not returndata["check"]:
						check=False
						errordata[fullkey]={}
						errordata[fullkey][returndata["rulename"]]=returndata["errordata"].replace(":key",f"'{fullkey.split(".")[-1]}'")
						if not firsterror:
							firsterror=returndata["errordata"].replace(":key",f"'{fullkey.split(".")[-1]}'")
						if not checkall:
							break
						if "bail" in testrulelist:
							bailstop=True

	# 回傳結果
	if check:
		return {
			"success": True,
			"data": data,
			"error": None
		}
	else:
		return {
			"success": False,
			"data": errordata,
			"error": firsterror
		}