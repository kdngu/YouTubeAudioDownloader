import youtube_dl
import PySimpleGUI as sg
import sys
import os

def window():
    #Define Gui Layout
    layout = [
        [sg.Text('Enter the YouTube link: ')], 
        [sg.InputText(key='link'), sg.Button('Clear')],
        [sg.Text('Select your download location: ')], 
        [sg.InputText(key = 'folder'), sg.FolderBrowse()],
        [sg.Button('Download'), sg.Button("Cancel")],
        [sg.Text('Progress: ')], 
        [sg.InputText(key='textbox')],
    ]
    
    #Initialize GUI Window
    window = sg.Window('YouTube Downloader', layout, size=(400,200))
    
    try:
        while True:
            event, values = window.read()
            #If user closes window or clicks the 'cancel' buttons
            if event == sg.WIN_CLOSED or event == 'Cancel':	
                break
            
            #Clear window if user clicks 'Clear Button'
            if event == 'Clear':
                window.Element('link').Update('')
                window.Element('folder').Update('')
                window.Element('textbox').Update('')      
                
            #If the user clicks the 'Download' button
            if event == 'Download':
                
                #Update 'Progress' textbox
                window.Element('textbox').Update('Downloading!')
                window.Refresh()
                
                video_url = values['link']
                video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
                download_location = values['folder']
                
                #FFmpeg options for download and conversion
                options = {
                'format': 'bestaudio/best',
                'keepvideo' : False,
                'outtmpl' : '{}/{}.{}'.format(download_location, video_info['title'], video_info['ext']),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }]
                }

                #Download and convert YouTube video to mp3 format
                with youtube_dl.YoutubeDL(options) as ydl:
                    ydl.download([video_info['webpage_url']])
                
                window.Element('textbox').Update('Complete!')
                
    #Throw Popup Exception for Errors
    except Exception as e:
        window.Element('textbox').Update('') 
        sg.popup_error(f'Error', e)


if __name__ == "__main__":
    window()