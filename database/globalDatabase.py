import redis

keyFormat = 'global_{0}'
globalRedisDB = redis.StrictRedis( '127.0.0.1', 6379 )#TODO: move to config file
global_count_key = 'global_count'
project_list_key = 'project_list'
user_list_key = 'user_list'

def getGlobalCount():
	if globalRedisDB.get(global_count_key) == None:
		globalRedisDB.set(global_count_key, 0)

	return int(globalRedisDB.get(global_count_key))
	
def incrementGlobalCount():
	globalRedisDB.incr(global_count_key)

def addToUserList(userId):
	key = _globalKey(user_list_key)
	globalRedisDB.lpush( key, userId )

def removeFromUserList(userId):
	key = _globalKey(user_list_key)
	globalRedisDB.lrem( key, 0, userId )

def getUserListAll():
	key = _globalKey(user_list_key)
	return globalRedisDB.lrange(key, 0, -1)

def addProjectIdToProjectList(projectId):
	key = _globalKey(project_list_key)
	globalRedisDB.lpush( key, projectId )

def removeProjectIdFromProjectList(projectId):
	key = _globalKey(project_list_key)
	globalRedisDB.lrem( key, 0, projectId )

def getProjectListAll():
	return getProjectListRange(0, -1)

def getProjectListRange(start, end):
	key = _globalKey(project_list_key)
	return globalRedisDB.lrange(key, start, end)

#this function probably won't ever be needed
def moveProjectToFront(projectId):
	key = _globalKey(project_list_key)
	atom = globalRedisDB.pipeline()
	atom.lrem(key, 1, projectId)
	atom.lpush(key, projectId)
	atom.execute()

def _globalKey(inputStr):
	return keyFormat.format(inputStr)
