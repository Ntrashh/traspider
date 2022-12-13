import string

from traspider.util.trajson import ast


class Lexical:
	START_IDENTIFIER = set(string.ascii_letters + '_')
	VALID_IDENTIFIER = set(string.ascii_letters + string.digits + '_')
	VALID_NUMBER = set(string.digits)
	TOKENS = {
		'/': "line",
		"@": "flag",
		"*": "star",
		"]": "rbrackets",
	}

	def __init__(self, rule):
		self.__posit = 0
		self.__rule = rule
		self.__rule_len = len(self.__rule)
		self.__rule_list = list(self.__rule)
		self.__curr = self.__rule_list[self.__posit]
		self.__index = 0
		self.__lexical_word = list(self.lexical())

	def lexical(self):
		# 循环知道__curr为None
		while self.__curr is not None:
			# 如果_curr在TONKENS中
			if self.__curr in self.TOKENS:
				yield {'type': self.TOKENS[self.__curr],
					   'value': self.__curr,
					   'start': self.__posit, 'end': self.__posit + 1}
				self.__next()
			# 如果__curr 在 START_IDENTIFIER
			elif self.__curr in self.START_IDENTIFIER:
				# 记录当前字符的起始位置
				start = self.__posit
				buff = self.__curr
				while self.__next() in self.START_IDENTIFIER:
					buff += self.__curr
				yield {'type': 'unquoted_identifier', 'value': buff,
					   'start': start, 'end': start + len(buff)}
			elif self.__curr == "[":
				yield {'type': "lbrackets",
					   'value': self.__curr,
					   'start': self.__posit, 'end': self.__posit + 1}
				self.__next()
		yield  {'type': 'eof', 'value': '', 'start': self.__posit, 'end': self.__posit}

	def __next(self):
		"""
		返回规则列表中下一个元素
		:return:
		"""
		# 如果当前指针等于规则列表
		if self.__posit == self.__rule_len - 1:
			self.__curr = None
		else:
			# 将指针加1 返回下一个内容
			self.__posit += 1
			self.__curr = self.__rule_list[self.__posit]
		return self.__curr


	def convert_to_ast(self):
		init_word = self.__get_lexical()
		self.__add_index()
		nud_function = getattr(
			self, f'_type_{init_word["type"]}')
		left = nud_function(init_word["value"])

		curr_type = self.__get_lexical_type()
		next_lex_fun = getattr(
			self, f'_type_{curr_type}',None)
		if curr_type != "eof":
			if next_lex_fun is None:
				raise TypeError('<Attributes not supported for parsing>')
			else:
				self.__add_index()
				left = next_lex_fun(left)
				curr_type = self.__get_lexical_type()
		return left

	def __get_lexical(self,index=0):
		return self.__lexical_word[self.__index+index]

	def __get_lexical_type(self,index=0):
		return self.__lexical_word[self.__index+index]["type"]




	def __add_index(self):
		self.__index += 1


	def _type_unquoted_identifier(self,value):
		return ast.field(value)

	def _type_line(self,left):
		"""如果标签是line进入这个方法"""
		# 如果下一个标签是类型是不是star
		if not self.__get_lexical_type() == "star":
			right = self._parse_lin_rlbrack()
			if left['type'] == 'subexpression':
				left['children'].append(right)
				return left
			else:
				return ast.subexpression([left, right])

	def _parse_lin_rlbrack(self):
		type = self.__get_lexical_type()
		if type in ["unquoted_identifier", "star"]:
			return self.convert_to_ast()

	def _parse_arr_rlb(self):
		if self.__get_lexical_type() == "line":
			self.__verity_tag("line")
			right = self._parse_lin_rlbrack()
		return right


	def _type_lbrackets(self,left):
		self.__verity_tag('star')
		self.__verity_tag('rbrackets')
		right = self._parse_arr_rlb()
		return ast.arrexpression(left, right)

	def __verity_tag(self,tag):
		if self.__get_lexical_type() == tag:
			self.__add_index()
		else:
			# TODO 处理错误
			raise TypeError('<Syntax error, the list type only supports [*] expressions>')

class Visit:
	def __init__(self):
		self._method_cache = {}

	def visit(self,node,json_data):
		node_type = node['type']
		method = self._method_cache.get(node_type)
		if method is None:
			method = getattr(self,f"visit_{node_type}")
			self._method_cache[node_type] = method
		return method(node, json_data)

	def visit_subexpression(self, node, value):
		result = value
		for node in node['children']:
			result = self.visit(node, result)
		return result

	def visit_field(self, node, value):
		try:
			return value.get(node['value'])
		except AttributeError:
			return None

	def visit_arrexpression(self, node, value):
		base = self.visit(node['children'][0], value)
		if not isinstance(base, list):
			return None
		collected = []
		for element in base:
			current = self.visit(node['children'][1], element)
			if current is not None:
				collected.append(current)
		return collected


