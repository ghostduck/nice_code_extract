# Decorator

This is a write-up article after checking the decorator feature article in realPython.

## What is decorator in Python?

We try to modifiy an existing function while preserving it.

We may pass in some new parameters through **closure** to change how we call the original function (but we probably do not change anything inside the original function.)

## Summary

Useful boilerplate for decorators not excepting arguments.

```python
# Decorator declaration:
import functools

def decorator(original_func):
    @functools.wraps(original_func)
    def modified_func(*args, **kwargs):
        # Do something before
        value = original_func(*args, **kwargs)  # pass the original_func here with closure
        # Do something after
        return value
    return modified_func
    # Note: modified_func is called decorator_wrapper in the article

# Decorator usage example:
@decorator
def func(can_have_params_for_func):
    # ... # do you things

# This means func = decorator(func)
# decorator() will be excuted: func = modified_func

# Like a Maths equation:
#  func = decorator(func)  # decorator() will be executed
#  func = modified_func  # now it points to the modified_func, which contains the original func()

# Setup is completed at this stage.

# ...
func(some_params)

# So under the surface, we just executed the modified/decorated func() under the old name of func
# func() = modified_func()

# *** IMPORTANT reminder:  modified_func contains the original func() inside!!! ***
# This is why decorator is so powerful.
```

This is the boilerplate of decorator accepting optional arguments. I consider this as the ultimate version.

```python
import functools

def name(_original_func=None, *, kw1=val1, kw2=val2, ...):
    def decorator_name(original_func):
        @functools.wraps(original_func)
        def modified_func(*args, **kwargs):
            # Do something before
            # Note that we can use keyword arguments from name() - closure
            value = original_func(*args, **kwargs)
            # Do something after
            return value

        return modified_func

    if original_func is None:
        return decorator_name
    else:
        return decorator_name(_original_func)

# Decorator usage example:
# --- with arguments---
@name(count_time=5)
def another_func(can_have_params_here, does_not_matter):
    #...

# Equal to
# another_func = name(count_time)(another_func)
#                                 ^^^^^^^^^^^^
# In the original article they did not explicitly specify this is happening.

# Continue executing name(count_time). Inside name(), _original_func is None when we have the keyword params. (Don't ask me why. Probably Python design.)
# another_func = decorator_name(another_func)
#                ^^^^^^^^^^^^^^
# It is returned from the "if original_func is None:" part

# It is now the decorator we are familiar with. Continue with the run.
# another_func = modified_func

# --- no arugment ---
@name
def some_func():
    #...

# Equal to
# some_func = name(some_func)

# When we use the decorator without arguments, some_func is passed to _original_func

# We want to achieve this - "some_func = decorator_name(some_func)"
# So name(some_func) can directly return decorator_name(some_func) in the last if part.

# Show the whole flow now from the beginning
# some_func = name(some_func)
# some_func = decorator_name(some_func)  # from the last if part
# some_func = modified_func
```

## Detailed explanation

Read these when you are new to decorator. Or when I forget everything and want to refresh my memory.

So let's start with showing how can we "modify" a function without changing that function directly. (Not using a code editor!)

### Do the same thing not using decorator

```python
# Easy to understand but not the @decorator we know
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = my_decorator(say_whee)

>>> say_whee()
Something is happening before the function is called.
Whee!
Something is happening after the function is called.

# Original say_whee is called and got "covered" by my_decorator
# say_whee is now assigned to the wrapper in my_decorator (which calls the old say_whee)
```

We can do these since functions in Python are the same as other normal objects, like tuples, floats, integers, strings ...

### Decorator - @decorator

Now check the @decorator we know - the syntactic sugar

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")
```

Just think that the decorator will cover the smaller function. Or like an add-on. It is like wearing new dinosaur shirt / equiping new armor (and give you extra ability in game) - it should still be the original thing.

![Bocchi Dino](images/bocchi.jpg)

Logically it is like:

```txt
@my_decorator(
def say_whee():
    print("Whee!")
)
```

Same as `say_whee = my_decorator(say_whee)` in Python internally.

### More examples

Look at more examples of more realistic decorators. This one call the decorated function twice, while preserving its original parameter.

```python
# In decorators.py
# Still incomplete... yet
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

# In driver program
from decorators import do_twice

@do_twice
def greet(name):
    print(f"Hello {name}")

@do_twice
def say_whee():
    print("Whee!")

>>> say_whee()
Whee!
Whee!

>>> greet("World")
Hello World
Hello World
```

However, the return value is lost. The fix:

```python
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)  # HERE!!!
    return wrapper_do_twice
```

Still something else can be improved - we want to retain info on `func`.

```python
import functools  # new!

def do_twice(func):
    @functools.wraps(func)  # new!
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

# So these info are now more meaningful

>>> say_whee
<function say_whee at 0x7ff79a60f2f0>

>>> say_whee.__name__
'say_whee'

>>> help(say_whee)
Help on function say_whee in module whee:

say_whee()
```

### Very good boilerplate template

So this is the good boilerplate template of decorators. Good enough but still not the ultimate form.

```python
# This decorator does not take parameters.

# Summary:
# @decorator
# def func(can_have_params_for_func):

# This means func = decorator(func)
# So decorator() will be excuted: func = modified_func
# *** Note that modified_func contains the original func() inside ***

# So func() - when we execute the function, modified_func() will be executed, which will involve the original func().

# So we can say that we use decorator to pass/move our original function into a wrapper function

import functools

def decorator(original_func):
    @functools.wraps(original_func)
    def modified_func(*args, **kwargs):
        # Do something before
        value = original_func(*args, **kwargs)
        # Do something after
        return value
    return modified_func
    # Note: modified_func is decorator_wrapper in the article
```

### The ultimate boilerplate template

I consider this as the ultimate form. Use this when you have arguments for decorators.

```python
import functools

def name(_func=None, *, kw1=val1, kw2=val2, ...):
    def decorator_name(func):
        @functools.wraps(func)
        def modified_func(*args, **kwargs):  # originally named wrapper_repeat
            # Do something before
            value = func(*args, **kwargs)
            # Do something after
            return value

        return modified_func

    if _func is None:
        return decorator_name
    else:
        return decorator_name(_func)
```

### Explanation on the ultimate boilerplate

Some explanation to the boilerplate. Use the `repeat` decorator as example.

```python
def repeat(_func_passed=None, *, num_times=2):
    def decorator_repeat(func):

        @functools.wraps(func)
        def modified_func_repeat_with_num_times(*args, **kwargs):  # originally named wrapper_repeat
        # ...
        return modified_func_repeat_with_num_times

    if _func_passed is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func_passed)

@repeat(num_time=3)
def greet(name):
    print(f"Hello {name}")

@repeat
def say_whee():
    print("Whee!")
```

When we define `greet()` with the decorator `@repeat(num_times=3)`, `repeat()` is called with keyword arguments. Therefore `_func_passed` is `None`. (Positional arguments must be passed first before the keyword arguments.)

We passed `num_time` (with the value of 3) to that `decorator_repeat`.

So check the formula...

```text
# _func is None in repeat()
# !!! This is the most important hint -- greet is still passed to the function, but you don't see it in repeat() !!!
greet = repeat(num_time=3)(greet)

# repeat(3) returns the decorator_repeat which runs original greet in last part
greet = decorator_repeat(greet)

# num_time with value of 3 is sneaked into decorator_repeat / modified_func_repeat_with_num_times
greet = modified_func_repeat_with_num_times
greet() = modified_func_repeat_with_num_times()
```

Compare to the default `repeat`. `say_whee` is passed to `repeat`.

```text
say_whee = repeat(say_whee)  # when there is no num_time in repeat
say_whee = decorator_repeat(say_whee)  # from the return statement in last part
say_whee = modified_func_repeat_with_num_times
say_whee() = modified_func_repeat_with_num_times()
```

### Decorator chaining

We can chain decorators!

Do note that even if we keep chaining decorators, we still only have same old function pointing to the "original function with some additions" .

**We are not forking our old function by chaining decorator.**

Copying the example from the realpython website.

```python
from decorators import debug, do_twice

@debug
@do_twice
def greet(name):
    print(f"Hello {name}")
```

Under the surface it is...

```txt
greet = debug(do_twice(greet))
```

If we reverse the order, we will see the debug message twice. We probably don't want it so be careful when chaining.

```python
from decorators import debug, do_twice

@do_twice
@debug
def greet(name):
    print(f"Hello {name}")

>>> greet("Eva")
Calling greet('Eva')
Hello Eva
'greet' returned None
Calling greet('Eva')
Hello Eva
'greet' returned None
```

## Actual examples

The following one is a practical one. Copy from realPython timer example.

```python
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

@timer
def slow(delay=1):
    time.sleep(delay)
    return 'Finished!'

print(slow())
Finished 'slow' in 1.0011 secs
Finished!

print(slow(3))
Finished 'slow' in 3.0031 secs
Finished!

```

## References

<https://realpython.com/primer-on-python-decorators/>

<https://github.com/realpython/materials/tree/master/primer-on-python-decorators>
