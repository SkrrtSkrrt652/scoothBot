![scoothbot-logos](https://user-images.githubusercontent.com/38008146/123531741-b0cdbd80-d724-11eb-9109-2ba4f05f04c1.jpeg)

<h1 align="center" >
  <span style="color : blue;">scootBot</span>
</h1>


## Overview

scoothBot is a fast and useful discord bot that uses the dicord.py API that can save teachers hours of work and make online classes a more rewarding experience for the students. The name is a portmanteau of school, smooth, and bot.
When we set out to build a project for the education track, we were trying to bridge the disconnect in virtual classes between peer communication and actual lectures. In a school classroom, there is great overlap between these two. Students socialize amongst themselves in between different classes (and sometimes during a class 😶). Most times they just chat it up, but very often, they help each other out with material in the curriculum. That element of peer learning and classroom socialization has been mostly lost in the Zoom era. A platform such as discord which allows a server with text and voice channels is great for this, but just the platform alone would not be worth the switch to it. With this bot however, we have come to believe that the future of the online classroom is definitely on a platform with bots, and it is very much worth the effort to switch.

## APIs Used 
discord.py
rapidAPI(Google API, Bing Image Search API and Random Stuff API)

## Bot commands 
All schoothBot commands begin with '$'.

  ### _Initiate text attendance_:
  Syntax: `$att poll`

  ### _Initiate automatic voice-chat attendance_:
  Syntax: `$att voice`

  ### _Show attendance data_:
  Syntax: `$att show`

  ### _Save attendance as a csv file_:
  Syntax: `$att show save`

  ### _Bot's Random Cringey jokes:_
  Syntax:` $cringe`

  ### _Fun trivia:_
  Syntax:` $question <CATEGORY> <NUMBER OF QUESTIONS>`

  ### _Quick search on a certain topic:_
  Syntax:` $search "<QUERY>" <NUMBER OF RESULTS>`

  ### _Create a popquiz:_
  Syntax:` $popquiz create`

  ### _Start popquiz:_
  Syntax:` $popquiz throw`

  ### _Reveal answers to the quiz:_
  Syntax:` $popquiz reveal`
