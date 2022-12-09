from asyncio import Queue


class Scheduler:
	def __init__(self):
		self.queue = Queue()

	async def next_request(self):
		"""
		取出下一个请求的对象
		:return:
		"""
		return await self.queue.get()

	async def add_scheduler(self,request):
		"""
		将Request对象加入到调度器中
		:param request:
		:return:
		"""
		await self.queue.put(request)

	async def scheduler_qsize(self):
		"""
		查看当前调度器中的所有任务
		:return: 返回queue队列中的任务数
		"""
		return self.queue.qsize()
