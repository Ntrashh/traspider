import asyncio
import aiomysql
from loguru import logger


class AioMysql:

	def __init__(self, setting):
		self.setting = setting
		self.table_name = setting["table"]

	async def register(self, setting):
		'''
        初始化，获取数据库连接池
        :return:
        '''
		try:

			pool = await aiomysql.create_pool(host=setting["host"], port=setting["port"],
											  user=setting["user"], password=setting["password"],
											  db=setting["db"], autocommit=False)
			logger.info(f"{setting['host']}:{setting['port']}@{setting['db']}链接成功！")
			return pool
		except asyncio.CancelledError:
			raise asyncio.CancelledError
		except Exception as ex:
			logger.error("mysql数据库连接失败：{}".format(ex))

	async def get_curosr(self):
		'''
        获取db连接和cursor对象，用于db的读写操作
        :param pool:
        :return:
        '''
		pool = await self.register(self.setting)
		conn = await pool.acquire()
		cur = await conn.cursor()
		return conn, cur

	async def batchInsert(self, values):
		# 第一步获取连接和cursor对象
		conn, cur = await self.get_curosr()
		try:
			SQL = self.__generate_sql(values)
			# 将字典类型转为
			values = [self.__dict_to_tuple(item) for item in values]
			# 执行sql命令
			await cur.executemany(SQL, values)
			await conn.commit()
			logger.info(f"新增{cur.rowcount}条数据")
			# 返回sql执行后影响的行数
			return cur.rowcount
		finally:
			# 最后不能忘记释放掉连接，否则最终关闭连接池会有问题
			# await pool.release(conn)
			pass

	def __dict_to_tuple(self, item):
		if isinstance(item, dict):
			return tuple(item.values())
		else:
			raise TypeError("item type is not dict")

	def __generate_sql(self, values):
		"""
        生成sql语句
        :param values:
        :return:
        """
		if isinstance(values, list) and len(values) > 0:
			item = values[0]
		else:
			item = values
		sql = f"insert into {self.table_name}(" + self.__generate_key(
			item) + f") values ({','.join(['%s' for i in item.keys()])})"
		return sql

	def __generate_key(self, item):
		""" 生成key部分的sql语句"""
		sql = ""
		for index, key in enumerate(item.keys()):
			tag = ","
			if index == len(item.keys()) - 1:
				tag = ""
			sql += f"{key}{tag}"
		return sql

	async def inspection_conn(self):
		"""
		检测mysql是否链接正常
		:return:
		"""
		if 0 < list(self.setting.values()).count("") < 6:
			logger.error(f"mysql配置中有字段为空:{[key for key, val in self.setting.items() if val == '']}")
			return False
		elif list(self.setting.values()).count("") == 6:
			pass
		else:
			if not isinstance(self.setting["port"], int):
				logger.error("port字段必须是int类型")
				return False
			pool = await self.register(self.setting)
			if not pool is None:
				logger.info("mysql初始化正常")
				return True
			else:
				logger.error("mysql初始化失败")
				return False
