"""Downloads the Publicly available submissions of any codechef user.
   Private submissions can also be downloaded by provinding login credentials."""

import requests
from lxml import html
from bs4 import BeautifulSoup
import os,sys,traceback


#Establishing session

session_requests = requests.session()

login_url = "https://www.codechef.com/"

result = session_requests.get(login_url)


#Obtaining Authenticity_token

tree = html.fromstring(result.text)

authenticity_token = list(set(tree.xpath("//input[@name='form_build_id']/@value")))[0]




def parse_html(url,logout=0):
    """ Parses HTML of the Given URL.
    
    Args:
            url = URL of the webpage(str)

    Returns:
            Parsed HTML of the give URL
    """

    try:

        result = session_requests.get( url,  headers = {"referer":login_url,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}  )

        if logout == 0:

            raw_html=result.content

            soup = BeautifulSoup(raw_html,"lxml")

            return soup

    except requests.HTTPError  as e: 

            print("request exception",e)



Directory_Changed = False

def file_handling(file_name,contents,count):  
    """ Creates new file and updates log file.
    Args:
        file_name = Name of the file with suitable extension (str)
        contents = Contents to be Written onto the file (str)
        count = Specifies the number of files successfully downloaded
    """

    if os.path.isfile(file_name) ==  False:

        fout = open(file_name,"a")

        for content in contents:

            fout.write(content.text)

            fout.write("\n")

        fout.close()

    log = open("logfile.txt","w")

    log.write(str(count))

    log.close()  



def print_user_details(name,rating,numsolved):
    """Prints User Details.
    name = Name(or ID) of the User
    rating = Current rating of the user
    numsolved = Number of problems solved by the user
    """

    print("User Name: ",name)

    print("User Rating: ",rating)

    print("Number of problems solved Fully: ", numsolved)




def main(userhandle,pwd=None):
    """ Main function of the module.It crawls the user profile page and downloads successful submissions
        made by the user in appropiate file format.
    
    Command-line Args: 
        argv[1] = userhandle(compulsory)
        argv[2] = password(optional)

    """


    try:

        if pwd!=None:

                #Obtaining CodeChef Account Details

                username = userhandle

                password = pwd


                #Creating Payload to be Submitted

                payload = {
                    "name": username, 
                    "pass": password, 
                    "form_build_id": authenticity_token,
                    "form_id":"new_login_form"
                }       
        

                #Posting necessary info to login
        
                result = session_requests.post(

                    login_url, 

                    data = payload, 

                    headers = {"referer":login_url,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                )


        #Obtaining Username and Opening user profile

        username = userhandle    

        url="https://www.codechef.com/users/" + username


        #Parsing  Codechef profile of the User
    
        soup = parse_html(url)

        #Creating a new Directory to store files 

        if not os.path.exists(username):

            os.makedirs(username)

        #Changing current directory to the created directory

        global Directory_Changed

        if Directory_Changed == False:
            
             os.chdir(username)

             Directory_Changed = True

             #Creating log file to keep track of Downloaded files

             if os.path.isfile("logfile.txt") ==  False:

                 log = open("logfile.txt","w")

                 log.write("0")

                 log.close()         


        #Obtaining User Name ,Rating,Number of Problems Solved

        User_Profile_Container = soup.findAll("div",{"class" : "user-details-container" })

        User = User_Profile_Container[0].header.h2.text


        Rating_Container =  User_Profile_Container[0].findAll("a",{"class" : "rating" })

        Rating = Rating_Container[0].text

        problem_solved_container = User_Profile_Container[0].findAll("section",{"class":"rating-data-section problems-solved"})

        Fully_Solved_Problem_List = problem_solved_container[0].div.article.findAll("a")

        Problem_count = len(Fully_Solved_Problem_List)


        #Printing User Details

        print_user_details(User,Rating, Problem_count)


        #Finding Number of Files already Downloaded

        log = open("logfile.txt","r")

        Downloaded_Already = log.read()

        start=int(Downloaded_Already)    

        log.close()


        #Downloading Files

        Files_Downloaded = 0

        for count in range(start,Problem_count):

            problem = Fully_Solved_Problem_List[count]

            Problem_Name = problem.text

            problem_url = "https://www.codechef.com" + problem["href"]

            soup = parse_html(problem_url)

            Submission_container = soup.findAll("div",{"class:","tablebox-section"})

            Submission_table = Submission_container[0].table.tbody.findAll("tr")

            problem_id = " "

            #Find ID of the AC problem

            for AC_Problem in Submission_table:
                
                status = AC_Problem.findAll('td',{'width':'51'})

                if status[0].span.img["src"] == '/misc/tick-icon.gif':

                    problem_id = AC_Problem.td.text
                    
                    break

            try:

                solution_url = "https://www.codechef.com/viewsolution/" + problem_id

                soup = parse_html(solution_url)

                solution_container = soup.findAll("pre")

                Extention = solution_container[0]["class"][0]    

                Contents =  solution_container[0].findAll("li")

                print("Downloading Problem ",count+1," : ",Problem_Name," ................................ ")

                file_handling(Problem_Name+"."+Extention,Contents,count)   

                Files_Downloaded += 1

            except requests.HTTPError  as e: 

                print("Please try again after sometime :(")

                os.sys.exit()

            except KeyboardInterrupt:

                print("\nStopping Process......You can resume later :)")

                parse_html('https://www.codechef.com/logout',1)

                os.sys.exit()
        
            except:

                print("This file cannot be downloaded :(")

                log = open("logfile.txt","w")

                log.write(str(count))

                log.close()      


        print("Downloaded ",Files_Downloaded,"files successfully :)")

        parse_html('https://www.codechef.com/logout',1)

   
    except KeyboardInterrupt:

        print("\nStopping Process......You can resume later :)")

        parse_html('https://www.codechef.com/logout',1)

    except requests.HTTPError  as e: 
    
        print("request exception",e)

        parse_html('https://www.codechef.com/logout',1)

    except SystemExit as e:

        print("\n")

    except:
        #For debugging purpose
        
        #print(traceback.print_exc()) 

        print("Some Error Occurred :( \nPlease Try again after sometime")

        parse_html('https://www.codechef.com/logout',1)


if __name__ == "__main__":

    if len(sys.argv) > 2:
        main(sys.argv[1],os.sys.argv[2])

    else:
        main(sys.argv[1])