
import hashlib

class Encrypt:

	@staticmethod
	def md5(str):
		hashlib_md5 = hashlib.md5()
		hashlib_md5.update(str.encode(encoding='utf-8'))
		return hashlib_md5.hexdigest()