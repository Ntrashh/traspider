import json

from traspider.util.trajson.lexical import Lexical, Visit


class TraJson(dict):

	def xpath(self,xpath_str):
		if isinstance(xpath_str,str):
			lexical = Lexical(xpath_str)
			ast_obj = lexical.convert_to_ast()
			visit = Visit()
			return visit.visit(ast_obj,self)














