# CodeChef-Crawler

<p><b>Usage:</b></p>
<ul>
<li>Clone the repository and extract the files</li>
<li>Run the script
<br><b>eg: python3 crawl.py username password  </b>    //    To download your submissions from <b>ongoing contests</b> <br>
    (or) just type <b>python3 crawl.py</b></li>
 <li>Then type the codechef username of the user whose sucessful submissions are to be downloaded</li>
 
 </ul>
 
 <hr>
 
 <p><b>Requirements:</b></p>
 <ul>
 <li>Python3 or greater</li>
 <li>Requests</li>
 <li>lxml</li>
 <li>bs4</li>
 </ul>
 
 <hr>
 
 <p><b>Features:</b></p>
 <ul>
 <li>Automatically creates a folder with username and downloads the files one by one </li>
 <li>Whenever the download is interrupted,the next time when the script is ran ,downloading resumes from the previous point
 </li>
 <li>Download process can be stopped by keyboard interrupt</li>
 </ul>
 
 
 
 <hr>
 
 <p><b>Note:</b></p>
 <ol>
 <li>Username and Password are not necessary to download problems that are publicly available.You can download successful submissions of <b>any user</b> by just entering their codechef username</li>
 <li>To download <b>your</b> ongoing contest submissions or submissions that are not publicly available ,Username and Password  not necessary</li>
 <li>Download process may be terminated due to http error (like 503).In such case,run script after sometime and download resumes from the previous point</li>
 
      
  
