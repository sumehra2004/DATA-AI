def login_required(func):
    def wrapper(*args,**kwargs):
        is_logged_in=True
        if is_logged_in:
            return func(*args,**kwargs)
        else:
            print("Please login to add products")
    return wrapper


def registration_required(func):
    def wrapper(*args, **kwargs):
        is_registered=True
        if is_registered:
            return func(*args)
        else:
            print("❌ Please register to view cart")
    return wrapper
