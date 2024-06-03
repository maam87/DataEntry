from tkinter import ttk


def Light_Theme():
    style = ttk.Style()

    # Style Label------------
    style.configure('Label', foreground='#3333ff', font=('New Times Roman', 14, 'italic'))
    style.configure('TLabel', foreground='#3333ff', font=('New Times Roman', 18, 'bold italic'))

    # Style Button-----------
    style.configure('TButton', foreground='#3333ff',
                    font=('New Times Roman', 16, 'italic'),
                    background='#FF8000',
                    disabledforeground='red',
                    disabledbackground='red')

    # Style RadioButton------
    style.configure('TRadiobutton', foreground='#3333ff', font=('New Times Roman', 14, 'italic'))

    # Style ComboBox---------
    style.configure('TCombobox', foreground='#3333ff', font=('New Times Roman', 14, 'italic'))

    # Style Treeview---------
    style.configure('Treeview', foreground='#066', font=('New Times Roman', 14, 'italic'))

    # Style Treeview Heading------
    style.configure('Treeview.Heading', foreground='#3333ff', font=('New Times Roman', 14, 'bold italic'))

    # Style Entry---------------
    style.configure('TEntry', foreground='#099', font=('New Times Roman', 14, 'italic'),
                    background='#e0e0e0')

    # Style Entry---------------
    style.configure('Treeview.field', foreground='#099', font=('New Times Roman', 14, 'italic'),
                    background='#e0e0e0')

    style.theme_use('clam')
    style.theme_settings('clam', {
        't.TButton': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', '#2b3e50')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'l.TLabel': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'lf.TLabelframe': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'lf.TLabelframe.Label': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'f.TFrame': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'cb.TCombobox': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'e.TEntry': {
            'configure': {
                'padding': (4, 4, 4, 4),'widthBorder': 0,'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        't.Treeview': {
            'configure': {
                'padding': (4, 4, 4, 4), 'widthBorder': 0, 'relief': 'flat', 'border': 0,
                'font': 'Courier 15 italic', 'background': 'green'
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'green'),
                                   ('pressed', 'white')],
                    'foreground': [('focus', 'red'),
                                   ('active', '#ff0000'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('pressed', '#2b3e50')]
                    }
        },
        't.Treeview.Heading': {
            'configure': {
                'padding': (4, 4, 4, 4), 'widthBorder': 0, 'relief': 'flat', 'border': 0,
                'font': 'Courier 14 bold italic'
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'red')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'r.TRadiobutton': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'r.TRadiobutton.Label': {
            'configure': {
                'padding': (4, 4, 4, 4), 'font': 'Courier 16 bold italic', 'widthBorder': 0,
                'relief': 'flat', 'border': 0
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
        'TScrollbar': {
            'configure': {
                'padding': (4, 4, 4, 4),
            },
            'map': {'background': [('active', '#4c9be8'),
                                   ('!disabled', '#2b3e50'),
                                   ('disabled', 'gray')],
                    'foreground': [('active', '#4e5d6c'),
                                   ('!disabled', '#ffffff'),
                                   ('disabled', '#f0ad4e'),
                                   ('focus', '#5cb85c')]
                    }
        },
    })
