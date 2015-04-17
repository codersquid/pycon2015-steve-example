# pycon2015-steve-example

This repo has the contents of the directory where I did work to push
pycon2015 videos to pyvideo.

Currently [steve](https://github.com/pyvideo/steve) uses vidscraper to scrape youtube,
and that doesn't work with channels or playlists. We've not had time to change steve
to rework it yet, and in the meantime I have some one-off youtube script that I use
to grab json data. Once I have that, I use parts of steve to save the data to json
files so that I can finish the process by using steve's command line interface.

For this example,
* I used the pyvideo.org admin to add a new category, PyCon US 2015. (this is not in the API)
* I tweaked things to massage the title, description, and speaker data from the PyCon2015 channel
* I used `steve-cmd webedit` to change a few titles (I found that I forgot about Lightning talks)
* and then I used `steve-cmd push` to push things to pyvideo.
* At the admin, I toggled everything from draft to live.
* I still had some names and titles to edit in pyvideo.org, when I noticed some dedups and some titles that could be improved -- I usually notice these when I'm watching some videos. For example, I corrected Titus Brown to C. Titus Brown, lvh to his full name, Vanderplas to VanderPlas, etc.
* When I watch videos and see find useful links that relate to the talks, I add those by hand. (this is not in the API)
