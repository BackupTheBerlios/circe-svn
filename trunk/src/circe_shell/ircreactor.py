wxreactor = None
reactor = None

def ImportWx():
    global wxreactor
    from twisted.internet import wxreactor
    wxreactor.install()

def ImportReactor():
    global reactor
    from twisted.internet import reactor

def Run():
    reactor.run()

def RegisterWxApp(app):
    reactor.registerWxApp(app)
