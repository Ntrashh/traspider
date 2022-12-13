from node_vm2 import VM

from traspider.util.exception import FileTypeUnsupported


class Node:
	def __init__(self, js_path=None):
		if js_path is None or js_path == "" or js_path.split(".")[-1] != "js":
			self.js_path = ""
		else:
			js_file = open(js_path, encoding="utf-8")
			self.js_path = js_file.read()

	def call_node(self, func_name, *args, **kwargs):
		if self.js_path == "":
			raise FileTypeUnsupported("<js file is empty or not a js file at all>")
		return self.__call_vm(func_name, *args, **kwargs)

	def __call_vm(self, func_name, *args, **kwargs):
		with VM() as vm:
			vm.run(self.js_path)
			return vm.call(func_name, *args, **kwargs)
