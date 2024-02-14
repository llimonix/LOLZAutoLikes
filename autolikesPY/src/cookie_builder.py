def build_cookie(cookies):
    return '; '.join([f'{key}={value}' for key, value in cookies.items()])
