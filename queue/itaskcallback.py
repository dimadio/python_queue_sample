class ITaskCallback(object):
    def call(self, User, ID):
        raise NotImplementedError()
