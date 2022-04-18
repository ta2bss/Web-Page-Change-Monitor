from pywebcopy import save_webpage

url = 'http://nodes.guru/'
download_folder = 'downloads/'

kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name'}

save_webpage(url, download_folder, **kwargs)