# pycon2015-steve-example

This repo has the contents of the directory where I did work to push
pycon2015 videos to pyvideo.

Currently [steve](https://github.com/pyvideo/steve) uses vidscraper to scrape youtube,
and that doesn't work with channels or playlists. We've not had time to change steve
to rework it yet, and in the meantime I have some one-off youtube script that I use
to grab json data. Once I have that, I use parts of steve to save the data to json
files so that I can finish the process by using steve's command line interface.

For this example,
* I used the pyvideo.org admin to add a new category, PyCon US 2015
* I tweaked things to massage the title, description, and speaker data from the PyCon2015 channel
* I used `steve-cmd webedit` to change a few titles (I found that I forgot about Lightning talks)
* and then I used `steve-cmd push` to push things to pyvideo.
* At the admin, I toggled everything from draft to live.
