from traspider.util.traerror import ElementError


class Element():
	def __init__(self,element):
		self.element = element

	def extract(self):
		return self.element

	def extract_first(self):
		if isinstance(self.element,list) and len(self.element) >0:
			return self.element[0]
		if isinstance(self.element,str):
			return self.element
		raise ElementError("element长度为0")

	def get_index(self,index):
		if isinstance(self.element,list) and len(self.element) >0:
			return self.element[index]
		if isinstance(self.element,str):
			raise ElementError("TypeError:对字符串使用get_index")
		raise ElementError("element长度为0")