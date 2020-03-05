import multiprocessing
import time

DEFAULT_TIMEOUT = 180
DEFAULT_RANGE = range(1,15)

class Timing:

    # https://stackoverflow.com/questions/14920384/stop-code-after-time-period
    @classmethod
    def timeout(cls, t, f, *args, **kwargs):
        p = multiprocessing.Process(target=f, name=f.__name__, args=args, kwargs=kwargs)
        p.start()
        p.join(t)
        if p.is_alive():
            p.terminate()
            p.join()
            return True
        return False

    @classmethod
    def test(cls, f, *args, note="", ns=DEFAULT_RANGE, t=DEFAULT_TIMEOUT, **kwargs):
        """Call f with successively higher n until it times out"""

        # Sometimes convenient to pass "None" to mean "pick your own default"
        ns = ns if ns else DEFAULT_RANGE
        t = t if t else DEFAULT_TIMEOUT

        print(f"====== Timing Test for {f.__name__} ======")
        if note:
            print(note)
        lastDuration = None
        for n in ns:
            print(f"  {f.__name__}({n}) ... ", end="")
            start = time.time()
            timedOut = cls.timeout(t, f, n, *args, **kwargs)
            end = time.time()
            duration = end-start

            ratio = 1
            if lastDuration:
                ratio = duration / lastDuration
            lastDuration = duration

            if not timedOut:
                print(f" {duration:8.4f}s ({ratio:.2f}x)")
            else:
                print(f" {duration:8.4f}s (>{ratio:.2f}x) timed out!")
                return

    @classmethod
    def waitFor(cls, t):
        time.sleep(t)
        return
