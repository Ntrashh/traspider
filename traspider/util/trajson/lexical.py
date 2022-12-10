import string


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
		# self.__next()

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


if __name__ == '__main__':
	lexical = Lexical("data/data[*]/data")
	for i in lexical.lexical():
		print(i)
