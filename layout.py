import PySimpleGUI as sg
# import PySimpleGUIQt as sg
yo1 = b'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'
sg.theme('DarkBlue')

def GUI():
    left_col = [
                [sg.Text('Image   Folder'), sg.In(size=(10,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
                [sg.Text('Data Base File'), sg.In(size=(10,1),  disabled=True, enable_events=True ,key='-DBfile-'), sg.FileBrowse( disabled=True)],
                [sg.Radio('Both side','Radio', enable_events=True, key='bside'),sg.Radio('Left side','Radio', enable_events=True, key='lside'),sg.Radio('Right side','Radio', enable_events=True, key='rside') ],
                [sg.Text('Count'),sg.Text(' '*5,key='num_of_image')],
                [sg.Listbox(values=[], enable_events=True, size=(30,15),key='-FILE LIST-')],
                [sg.Button('Analyse'), sg.Text('Resize to   W'), sg.In('380',key='-W-', size=(5,1)),sg.Text(' H'), sg.In('560',key='-H-', size=(5,1))],
                [sg.Text('Detection  %threshold for detection   '),sg.Slider((1,50), 4, 1,   orientation='h', size=(20, 12),enable_events=True, key='thresh_percent')],
                [sg.Multiline(size=(30, 5),  key='-MLINE-')],
                ]

    # For now will only show the name of the file that was chosen
    tab_Main = [

                  [sg.Image(key='-IMAGE-',size=(250,550)),sg.VSeperator(),sg.Image(key='IMAGE_p',size=(250,550)),]
                  ]
    images_col= [
                
                [sg.Image(key='-IMAGE-',size=(250,450))],
               ]
    tab_Setting = [
                [sg.Radio('None'      ,'Setting', enable_events=True, key='None',default=True)],
                [sg.Radio('Canny'     ,'Setting', enable_events=True, key='canny'),    sg.Slider((0, 255), 0, 1,   orientation='h', size=(20, 15),enable_events=True, key='canny_slider_a'),sg.Slider((0, 255), 30, 1, orientation='h', size=(20, 15), enable_events=True,key='canny_slider_b')],
                [sg.Radio('threshold ', 'Setting', enable_events=True, key='-THRESH-'), sg.Slider((0, 255), 6, 1, orientation='h', size=(39, 15),enable_events=True, key='-THRESH SLIDER-')],
                [sg.Radio('blur       ', 'Setting', enable_events=True, key='-BLUR-'), sg.Slider((1, 10), 1, 1, orientation='h', size=(39, 15),enable_events=True, key='-BLUR SLIDER-')],
                #                                                                               range=(None, None), default_value=None, resolution=None, tick_interval=None
                [sg.Radio('enhance', 'Setting'  , enable_events=True, key='-ENHANCE-'),sg.Text(' kernel_size '),sg.Slider((1,5), 1, 1,   orientation='h', size=(30, 12),enable_events=True, key='-ENHANCE SLIDER-')],
                [sg.Text('                      distance resolution '),sg.Slider((1,20), 1, 1,   orientation='h', size=(25, 12),enable_events=True, key='-distance resolution-') ],
                [sg.Text('                      angular resolution  '),sg.Slider((1,360), 180, 1,   orientation='h', size=(25, 12),enable_events=True, key='-angular resolution-') ],
                [sg.Text('                     min line'),sg.Slider((1,100), 1, 1,   orientation='h', size=(12, 12),enable_events=True, key='-min line-'),sg.Text('max line'),sg.Slider((1,100), 4, 1,   orientation='h', size=(12, 12),enable_events=True, key='-max line-')  ],
                
                [sg.Radio('contour',   'Setting', enable_events=True, key='contour')],
                [sg.Text('                         '),sg.Radio('type1',   'contour', enable_events=True,default=True, key='type1'),sg.Radio('type2',   'contour', enable_events=True, key='type2'),sg.Radio('type3',   'contour', enable_events=True, key='type3'),sg.Radio('type4',   'contour', enable_events=True, key='type4')],
                [sg.Radio('detec', 'Setting', enable_events=True, key='detec'), sg.Slider((1, 10), 1, 1, orientation='h', size=(39, 15),enable_events=True, key='-DETECT SLIDER-')], 
               ]
    tab_Result = [
                [sg.T('Left Side')],
                [sg.Multiline(size=(75, 15),  key='-MLINEL-')],
                [sg.T('Right Side')],
                [sg.Multiline(size=(75, 15),  key='-MLINER-')],
                 
               ]
    tab_Load = [
                [sg.Column(left_col, element_justification='left'), ]
                 
               ]           
    # ----- Full layout ----- 
    tab_group_layout_L = [[
                     sg.Tab('Load Data', tab_Load, ),
                     sg.Tab('Analyse selection', tab_Setting, ),
                      
                     ]]
    tab_group_layout_R = [[
                     sg.Tab('Main', tab_Main, ),
                     #sg.Tab('Setting', tab_Setting, ),
                     sg.Tab('Result', tab_Result, ),
                     ]]
     
    layout = [[sg.TabGroup(tab_group_layout_L,enable_events=True,key='TABG_L'),sg.TabGroup(tab_group_layout_R,enable_events=True,key='TABG_R'),]] 

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('Vineyard Analyzer', resizable=True,icon=yo1)
    #sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(text_justification='left',)
    # SetOptions(icon=None,
    # button_color=None,
    # element_size=(None, None),
    # button_element_size=(None, None),
    # margins=(None, None),
    # element_padding=(None, None),
    # auto_size_text=None,
    # auto_size_buttons=None,
    # font=None,
    # border_width=None,
    # slider_border_width=None,
    # slider_relief=None,
    # slider_orientation=None,
    # autoclose_time=None,
    # message_box_line_width=None,
    # progress_meter_border_depth=None,
    # progress_meter_style=None,
    # progress_meter_relief=None,
    # progress_meter_color=None,
    # progress_meter_size=None,
    # text_justification=None,
    # background_color=None,
    # element_background_color=None,
    # text_element_background_color=None,
    # input_elements_background_color=None,
    # input_text_color=None,
    # scrollbar_color=None,
    # text_color=None,
    # element_text_color=None,
    # debug_win_size=(None, None),
    # window_location=(None, None),
    # error_button_color=(None, None),
    # tooltip_time=None)
    return window.Layout(layout).Finalize()

if __name__ == '__main__':
    window=GUI()
    while True:
            event, values = window.read()
            print('\n event=[',event,']\n',values) if event != sg.TIMEOUT_KEY else None # cur_focus.Type
            
            if    event == 'close' or event is None:
                break


