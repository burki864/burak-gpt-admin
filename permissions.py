ADMINS = {
    "burakerenkisapro1122@gmail.com": "burki4509",
}
def check_admin(email, password):
    return ADMINS.get(email) == password
