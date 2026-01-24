import threading

def run_async(app, fn, *args):
    thread = threading.Thread(
        target=fn,
        args=(app, *args)
    )
    thread.daemon = True
    thread.start()
