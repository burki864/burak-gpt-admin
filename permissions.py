ADMINS = {
    "burakerenkisapro1122@gmail.com": "123456",
    "admin@gmail.com": "admin123"
}

def check_admin(email, password):
    return ADMINS.get(email) == password
