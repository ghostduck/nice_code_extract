#!/usr/bin/env python3

import time
import functools

def timer(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = f(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {f.__name__!r} in {run_time:.4f} secs")
        return result
    return inner

# --------------------------------------
# 3 and 2 will return to a real decorator
# 1 -> 0 -> 2 (send to 3 with params(payment) will have error)
# 3 is for functions without params

# special case: give a lot of money to 0 will be directed to KEKW

def useless_agent_deco0(payment=5000):
    print("0: Give me that {}".format(payment))
    if (payment >= 999999):
        print("0: FBI will steal that money from me. I will KEKW you")
        return do_something_agent
    else:
        print("0: I could reject you silently but I try to throw you away instead")
        return useless_agent_deco2(payment - 9000)

def useless_agent_deco1(payment=20000):
    print("1: Nice money {}".format(payment))
    print("1: I know nothing, try another agent. I will forward you")
    return useless_agent_deco0(payment - 10000)

def useless_agent_deco2(payment=20000):
    print("2: Thanks for the money {}".format(payment))
    if payment >= 400000:
        print("2: Wow, big money. I try to help")

        def residentSleeper_decorator(f):
            @functools.wraps(f)
            def modified_f(*args, **kwargs):
                result = f(*args, **kwargs)
                print(f"Zzz Zzz Zzz ResidentSleeper zzZ zzZ zzzZZZ")
                return result
            return modified_f

        print("2: See if this works")
        return residentSleeper_decorator

    else:
        print("2: No matter how much you pay. I do nothing and know nothing. I throw you to timer")
        return timer

def useless_agent_deco3(f):
    print("I don't take you money but don't do anything useful too")
    return timer(f)

def do_something_agent(f):
    def modified_f(*args, **kwargs):
        print("KEK: I will KEKW at you")
        result = f(*args, **kwargs)
        return result

    k = modified_f
    return timer(k)

@useless_agent_deco2(payment=6900000)
def gachiBASS():
    print("Billy gachiBASS I am not timed")

@useless_agent_deco2(payment=69)
def speedrun():
    print("Done")

@useless_agent_deco1(payment=90000)
def LUL():
    print("LUL")

@do_something_agent
def monkaS():
    print("monkaS I love sleeping zzzZZZ")
    time.sleep(2)
    print("Oh no I have to wake up monkaS")

@useless_agent_deco0(payment=99999999999)
def BibleThump(count=5):
    print("Help me {}".format("BibleThump " * count))

monkaS()
LUL()
speedrun()
gachiBASS()
BibleThump(15)
