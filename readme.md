<!-- 
TODO LIST:
- argparse (turn off selected analyzers; csv files paths; create charts; ...)
 -->
 
 #### HOW TO RUN
 
 ##### With docker: 
 <details>
   

Run in bash shell: 
 ```
 git clone https://github.com/yaxlie/youtube-trending-videos.git
 cd youtube-trending-videos
 docker build -t yt-trending .
 docker run -it yt-trending
 ```
 + *You can ommit **-it**, but then you will not see progress bar*.
 + *Maybe you will need to add **sudo** prefix.*
 
 </details>
 
  ##### Without docker: 
 <details>
   

 Just use docker, please :smile:
 <!-- TODO -->
  <details>
 If you really don't want to use docker, follow the steps in <b>Dockerfile</b>, but before that - <b>create virtual environment</b> for python.
  </details>
   
 
 </details>
