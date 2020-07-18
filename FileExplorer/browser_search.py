import webbrowser

input_ = 'value'

url = "https://www.google.com.tr/search?q={}".format(input_)
webbrowser.open_new_tab(url)
