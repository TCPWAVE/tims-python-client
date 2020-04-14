class IPAMException(Exception):

    def __init__(self, msg):
        super(IPAMException, self).__init__(msg)
        self.msg = msg


class APICallFailedException(IPAMException):

    def __init__(self, msg):
        super(APICallFailedException, self).__init__(msg)
        self.msg = msg


class UnsupportedMethodException(IPAMException):

    def __init__(self, msg):
        super(UnsupportedMethodException, self).__init__(msg)
        self.msg = msg

