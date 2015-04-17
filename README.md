# pycon2015-steve-example

This repo has the contents of the directory where I did work to push
pycon2015 videos to the [pyvideo pycon2015 category](http://pyvideo.org/category/65/pycon-us-2015).

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

Observations

When Carl has done events, adding the videos happens a lot quicker and we get more metadata because he has scripts and a webapp that links up the schedule data from a conference with the location of the videos on youtube (or vimeo, etc.) along with downloadable files (because he also pushes them to Rackspace cloudfiles and/or archive.org).

I'd like for people who upload videos to a location to give me data like that because it's neat to include the longer descriptions -- I've managed to hack it up by hand in the past when I'm more deeply involved in a conference. For example for US SciPy 2014 I wrote some scripts to mesh together descriptions from the schedule with the scraped youtube data because I was able to add a json api to the conference site to extract the schedule data in a machine readable format. That was cool because the speakers had written really nice and detailed abstracts with graphs and images. I was also able to do something similar for EuroPycon once because I got similar data from their system (frab.xml from the conference system), and they had also followed a convention in linking up uploaded files with the schedule data so that I could include download links for the conference.

Re-scraping a channel when videos are added later is still painful. there is no graceful way to handle that.
