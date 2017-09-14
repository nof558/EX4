import hashlib  # library for MD5 encryption
from firebase import firebase

DEBUG = False
# link instance to our DB in firebase
MyFirebase = firebase.FirebaseApplication('https://mylocation-cea11.firebaseio.com/', None)


# hash function that encrypte the password before
def hash_func(password):
    m=hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()


class shoeMakerRegister(object):
    def __init__(self):
        print()

    def create_new_user(self, _userName, password):
        shoeMaker = shoeMakerRegister()
        isExist = shoeMaker.isExistUser(_userName)
        if isExist:
            return 'The user already exists!!'
        else:
            MyFirebase.put('/users/' + _userName + '/', 'Password', hash_func(password))
            return 'User successfully added'

    def create_root_userName(self, userName, password):
        MyFirebase.put('/Admin/', userName + '/Password', password)

    # update extra info like adress mail phone number for user in DB
    def update_user_details(self, userName, password, mail, cellphone, country, city):
        shoeMaker = shoeMakerRegister()
        if shoeMaker.isExistUser(userName):
            MyFirebase.put('/users/', userName + '/Password', password)
            MyFirebase.put('/users/', userName + '/Email', mail)
            MyFirebase.put('/users/', userName + '/CellPhone', cellphone)
            MyFirebase.put('/users/', userName + '/Country', country)
            MyFirebase.put('/users/', userName + '/City', city)
            return 'userName ' + userName + ' updated Successfully'
        else:
            return userName + ' is not exist in the database'

    # delete user from DB by username

    def delete_exist_user(self, userName):
        shoeMaker = shoeMakerRegister()
        if shoeMaker.isExistUser(userName):
            MyFirebase.delete('/users/' + userName, None)
            return 'User deleted successfully.'
        else:
            return 'User is not in the database'

    # print all usernames in the DB

    def print_all_userNames(self):

        userName_list = MyFirebase.get('/users/', None)
        print("********LIST OF USERS************")
        if userName_list is None:
            print('Problem! [there are no users in the database!]')
        else:
            for user in userName_list:
                print(user)

    # check if the username exist in the DB

    def isExistUser(self, userName):
        result = MyFirebase.get('/users/', userName)
        if result is None:
            print("OK! [the userName doesn't exist in the system]")
            return False
        print("PROBLEM! [userName exist in the system]")
        return True

    def delete_databaste(self):
        MyFirebase.delete('/', None)
        return 'Delete all users from database'

# the admin log-in checking
def adminLogin():
    shoeMaker_registr_obj = shoeMakerRegister()
    isAdminLogin = False
    print("***-------------Manager Access Tool--------------------------***")
    print("please enter Manager username to enter the CLI:")
    log_user = input()
    while log_user.__eq__(""):
        print("### please try again! [with valid username] ###")
        log_user = input()
    print("please enter Manager Password to enter the CLI:")
    log_pass = input()
    while log_pass.__eq__(""):
        print("### please try again! [with valid password] ###")
        log_pass = input()
    if log_user.__eq__("Nof") and log_pass.__eq__("4699809"):
        isAdminLogin = True
        shoeMaker_registr_obj.create_root_userName(log_user, log_pass)
    while not isAdminLogin:
        print("### please try again! [Wrong username/password details] ###")
        adminLogin()
    return isAdminLogin

# respobsible for print the log-in Admin menu
def displayAdminMenu():
    if adminLogin():
        mainMenu()

# the CLI menu-ask the user which action he want to do and execute the action according to his input
def mainMenu():
    shoeMaker_registr_obj = shoeMakerRegister()
    print("**************This is the shoeMaker Manager Menu****************")
    print("Enter a number according to the action you want to do:")
    print("1.sign up new user in the system")
    print("2.make check if user exist in FireBase DB")
    print("3.remove user from the DB")
    print("4.Delete all the information in the DB")
    print("5.add or update user extra info")
    print("6.Print a List of all users in the DB")
    print("7.Quit Menu")
    print("******************************************************************")
    number = input()
    if number.__eq__("1"):
        print("Create new userName")
        print("Enter userName:")
        userName = input()
        while userName.__eq__(""):
            print("Error enter userName again:")
            userName = input()
        print("Enter Password:")
        password = input()
        while password.__eq__(""):
            print("Error enter password again:")
            password = input()
        print(shoeMaker_registr_obj.create_new_user(userName, password))
        mainMenu()
    elif number.__eq__("2"):
        print("Enter userName")
        userName = input()
        while userName.__eq__(""):
            print("Error enter userName again:")
            userName = input()
        print(shoeMaker_registr_obj.isExistUser(userName))
        mainMenu()
    elif number.__eq__("3"):
        print("Enter userName")
        userName = input()
        while userName.__eq__(""):
            print("Error enter userName again:")
            userName = input()
        print(shoeMaker_registr_obj.delete_exist_user(userName))
        mainMenu()
    elif number.__eq__("4"):
        print("Are you sure you want to delete database? prees Y/N")
        ok = input()
        while ok.__eq__(""):
            print("Error enter Y/N again:")
            ok = input()
        if ok.__eq__("Y"):
            print(shoeMaker_registr_obj.delete_databaste())
            mainMenu()
        else:
            mainMenu()
    elif number.__eq__("5"):
        print("Update section:")
        print("Enter userName")
        userName = input()
        while userName.__eq__(""):
            print("Error enter userName again:")
            userName = input()
        print("Enter Password")
        password = hash_func(input())
        while password.__eq__(""):
            print("Error enter password again:")
            password = input()
        print("Enter Email")
        email = input()
        print("Enter CellPhone")
        cellPhone = input()
        print("Enter Country")
        country = input()
        print("Enter City")
        city = input()
        print(shoeMaker_registr_obj.update_user_details(userName, password, email, cellPhone, country, city))
        mainMenu()
    elif number.__eq__("6"):
        print(shoeMaker_registr_obj.print_all_userNames())
        mainMenu()
    elif number.__eq__("7"):
        return

# the main function of the manager-display the CLI
def main():
    displayAdminMenu()


if __name__ == '__main__':
    main()
