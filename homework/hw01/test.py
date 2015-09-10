r = range(12,30)
riter = r.__iter__()
print(riter.__next__())
print(riter.__next__())
print(riter.__next__())
print(riter.__next__())
#print(riter.__next__())

class Meow:
	def __init__(self, start, finish):
		
		self.start = start
		self.finish = finish
	
	def __iter__(self):
		return MeowIter(self.start,self.finish)

class MeowIter(object):
	"""docstring for MeowIter"""
	def __init__(self, start,finish):
		
		self.now = start
		self.finish = finish
		
		
	def __next__(self):
		if self.now >= self.finish:
			#return None
			raise StopIteration
		else:
			tmp = self.now
			self.now += 2
			return tmp
		
# m = Meow(10,20)
# while True:
# 	val = m.next()
# 	if val is None:
# 		break
# 	print(val)
for i in Meow(10,20):
	print(i)

x = [1,2,3]
print(x.__iter__())



#homework assignment me: make a class that you can call to generate a list of 
#prime numbers in range!