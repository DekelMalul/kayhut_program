import requests
import sys
import getopt
import json
from tabulate import tabulate

'''
This function check if the given username and password are valid
'''
def git_user_validation(user,password):
    url = "https://api.github.com/user"
    respone = requests.request("Get", url, auth=(user,password))
    if respone.ok:
        print("User is valid")
    else:
        print("User or password isn`t valid", user)
        exit()

def org_check(org,user,password):
    url = "https://api.github.com/orgs" + org
    respone = requests.request("Get", url, auth=(user,password))
    if respone.ok:
        print("We found", org , "organization")
    else:
        print("It seems that your organization dosen't exist: ", org)
        exit()
        
def org_repos_info(org,user,password):
    url = "https://api.github.com/orgs/" + org + "/repos" 
    respone = requests.request("Get", url, auth=(user,password))
    repo_list = json.loads(respone.text)
    table_data = list()
    for repo in repo_list:
        reponame = repo.get("name")
        branch_url = ("https://api.github.com/repos/" + org + "/" +
        reponame +"/branches")  
        respone = requests.request("Get", branch_url, auth=(user,password))
        if not respone.ok:
            if respone.text.find("higher rate limit") != -1:
                print ("no more api calls for ", user)
                table = tabulate(table_data, headers = ["Repository","brauch count"])
                print(table)
                exit()
        if len (respone.text) == 2:
            table_data.append([reponame,0])
        else:
            branch_info = json.loads(respone.text)
            table_data.append([reponame,len(branch_info)])
    table = tabulate(table_data, headers = ["Repository","brauch count"])
    print(table)
    
def main():
     argv = sys.argv[1:]
     count = 0
     try: 
        opts, args = getopt.getopt(argv,"u:e:o:",["username =","email =","org ="])   
     except: 
        print("Enter valid parameters") 
     print(opts)  
     # Setting command line parameters
     for opt, arg in opts:
        if opt in ['-u', '--username']: 
            username = arg 
            count += 1
        elif opt in ['-e','--email']:
            username = arg
            count += 1
        elif opt in ['-o','--org']:
            org = arg
     if count == 0:
         print("enter email or username")
         exit()
     elif count == 2:
         print("Use email OR username not both")
         exit()
     try: 
         org
     except:
         print ("enter organization name")
         exit()
     password = input("enter user password or access token please: ")
      
     git_user_validation(username, password)
     org_check(org,username,password)
     org_repos_info(org,username,password)

main()
    