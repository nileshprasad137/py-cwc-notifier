import notify2
notify2.init('foo')
n = notify2.Notification('foo', 'bar')
n.timeout = 1000    # display duration
n.show()