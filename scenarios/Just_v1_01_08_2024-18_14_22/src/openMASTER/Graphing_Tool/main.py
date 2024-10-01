###########
# IMPORTS #
###########
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from tkinter.font import families
from PIL import Image, ImageTk
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
import customtkinter
import os
import json
import tempfile
import webbrowser
from sankey import create_sankey_diagram

###################
# System Settings #
###################
customtkinter.set_appearance_mode("Light") 
customtkinter.set_default_color_theme("blue") 

###########
# Sidebar #
###########
class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, width, *args, **kwargs):
        super().__init__(master, width=width, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Input variables
        self.width = width

        # Grid settings
        self.grid_rowconfigure(4, weight=1)

        # Company's logo
        logo_image = customtkinter.CTkImage(light_image=Image.open("Graphing_Tool\openMASTER_nobg.png"),      # Loading the logo image
                                  dark_image=Image.open("Graphing_Tool\openMASTER_nobg.png"),
                                  size=(self.width*0.7, self.width*0.35))
        self.logo_label = customtkinter.CTkLabel(self, image=logo_image, text="")               # display image with a CTkLabel
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))                           # Adding the logo label to the grid

        # Appeareance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # UI Scaling
        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    # Change UI Scaling Function
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Change Appearance Mode Function
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

###################
# Markdown Viewer #
###################
class MarkdownViewer(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Setting the font 
        self.font_style = font.Font(family="Helvetica", size=14)

        # Configure grid to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Converted output view
        self.viewer = HTMLLabel(self, background="white")
        self.viewer.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

        # Loading the input text
        self.input_text = self.load_md_file("Graphing_Tool\sankey_description.txt" )

        # Updating the output view
        markdown_to_html = Markdown()
        markdown_content = self.input_text
        html_content = markdown_to_html.convert(markdown_content)
        self.viewer.set_html(f'<p style="text-align:justify">{html_content}</p>')

    def load_md_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except Exception as e:
            messagebox.showerror("File Error", f"Can't open file: {filename}")

#####################
# Description Frame #
#####################
class Description_Frame(customtkinter.CTkFrame):
    def __init__(self, master, width, *args, **kwargs):
        super().__init__(master, width, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(border_width=-2)

        # Get the initial appearance mode
        self.appearance_mode = customtkinter.get_appearance_mode()

        # Input variables
        self.master = master
        self.width = width

        # Grid settings (2x1)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure(0, weight=2)

        # Description TextBox
        self.description_textbox = MarkdownViewer(self)
        self.description_textbox.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Load Data Button
        self.loadData_btn = customtkinter.CTkButton(self, width=150, text="Load Data", command=self.check_data_load)
        self.loadData_btn.grid(row=1, column=0,  columnspan=1, padx=(20, 0), pady=(10, 0), sticky="w")

        # Check Load Label
        self.check_label = tk.Label(self, text="")
        self.check_label.grid(row=1, column=0, padx=(175,20), pady=(10, 0), sticky="w")
        # Update the background color of the label
        self.update_label_bg_color()

    # Check Data Load Function
    def check_data_load(self):
        self.master.sankey_data = self.load_json_data().copy()
        if self.master.sankey_data is not None:
            self.check_label.configure(text="✓", fg="green")

    # Json Data Load Function
    def load_json_data(self):
        file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        else:
            return None
        
    def update_label_bg_color(self):
        fg_color = self.cget('fg_color')
        if self.appearance_mode == "Light":
            bg_color = fg_color[0]
        else:
            bg_color = fg_color[1]
        self.check_label.configure(bg=bg_color)

##################
# Units Selector #
##################
class UnitsSelector(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (5x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        # Variable to hold the selected unit
        self.selected_unit = tk.StringVar(value="TWh")
        self.selected_unit.trace('w', self.clear_custom_entry)

        # Radio Buttons (Units Selection)
        self.unit1_button = customtkinter.CTkRadioButton(self, text="TWh", variable=self.selected_unit, value="TWh")
        self.unit2_button = customtkinter.CTkRadioButton(self, text="MWh", variable=self.selected_unit, value="MWh")
        self.unit3_button = customtkinter.CTkRadioButton(self, text="KWh", variable=self.selected_unit, value="KWh")

        # Create the input box for custom unit
        self.custom_unit_entry = customtkinter.CTkEntry(self)
        self.custom_unit_label = customtkinter.CTkLabel(self, text="Other:")

        # Adding the buttons and entry to the grid
        self.unit1_button.grid(row=0, column=0, padx=(20, 0), pady=(0, 10), sticky="nsew")
        self.unit2_button.grid(row=1, column=0, padx=(20, 0), pady=(0, 10), sticky="nsew")
        self.unit3_button.grid(row=2, column=0, padx=(20, 0), pady=(0, 10), sticky="nsew")
        self.custom_unit_label.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="w")
        self.custom_unit_entry.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
        
        # Set an event to update the value of the custom radio button when text is entered
        self.custom_unit_entry.bind('<KeyRelease>', self.update_custom_value)

    def update_custom_value(self, event):
        custom_value = self.custom_unit_entry.get()
        self.custom_unit_label['value'] = custom_value
        if custom_value:
            self.selected_unit.set(custom_value)

    def clear_custom_entry(self, *args):
        if self.selected_unit.get() != self.custom_unit_entry.get():
            self.custom_unit_entry.delete(0, 'end')

##################
# Color Selector #
##################
class ColorSelector(customtkinter.CTkFrame):
    def __init__(self, master, color_label="Select Color Mode:", default_color="black", apply_btn=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Input Variables
        self.color_label = color_label
        self.default_color = default_color
        self.apply_btn = apply_btn
        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (5x2)
        self.grid_columnconfigure(0, weight=0)
        #self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        # List of predefined (preset) colors
        predefined_colors = ['black', 'blue', 'brown', 'cyan', 'darkgray', 'gray', 'green', 'lightgray', 'magenta', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']

        # Default color selection mode
        self.color_selection_mode = tk.StringVar(value="preset")

        # Label for color selection mode
        self.selection_mode_label = customtkinter.CTkLabel(self, text=self.color_label)
        self.selection_mode_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 10), sticky="nsew")

        # Radio Buttons for color selection mode
        self.preset_mode_button = customtkinter.CTkRadioButton(self, text="Preset Colors", variable=self.color_selection_mode, value="preset", command=self.toggle_color_selection_mode)
        self.preset_mode_button.grid(row=1, column=0, padx=(5, 0), pady=(0, 10), sticky="nsew")
        self.hex_mode_button = customtkinter.CTkRadioButton(self, text="Hex Color", variable=self.color_selection_mode, value="hex", command=self.toggle_color_selection_mode)
        self.hex_mode_button.grid(row=2, column=0, padx=(5, 0), pady=(0, 10), sticky="nsew")
        
        # Frame for predefined color selection
        self.preset_color_frame = customtkinter.CTkFrame(self)
        self.preset_color_frame.grid(row=3, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")
        self.preset_color_frame.configure(fg_color=master.cget('fg_color'), border_width=0)

        # OptionMenu for predefined color selection
        self.color_variable = tk.StringVar(self)
        self.color_variable.set(self.default_color)
        self.color_optionmenu = customtkinter.CTkOptionMenu(self.preset_color_frame, variable=self.color_variable, values=predefined_colors)
        self.color_optionmenu.pack()

        # Frame for hex color input
        self.hex_color_frame = customtkinter.CTkFrame(self)
        self.hex_color_frame.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Label and Entry for hex color input
        self.hex_entry = customtkinter.CTkEntry(self.hex_color_frame, placeholder_text="Enter Hex Color:")
        self.hex_entry.pack()

        # Button to apply chosen color
        self.apply_button = customtkinter.CTkButton(self, text="Apply", command=self.apply_color)
        if apply_btn:
            self.apply_button.grid(row=4, column=0, padx=(0, 0), pady=(0, 20), sticky="n")

    def toggle_color_selection_mode(self):
        mode = self.color_selection_mode.get()
        if mode == "preset":
            self.hex_color_frame.grid_remove()
            self.preset_color_frame.grid()
        elif mode == "hex":
            self.preset_color_frame.grid_remove()
            self.hex_color_frame.grid(row=3, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")

    def apply_color(self):
        mode = self.color_selection_mode.get()
        if mode == "preset":
            color = self.preset_color_frame.winfo_children()[0].get()
            self.configure(bg=color)
        elif mode == "hex":
            color = self.hex_color_frame.winfo_children()[1].get()
            if color:
                self.configure(bg=color)

#####################
# Background Selector
#####################
class BackgroundSelector(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (2x3)
        self.grid_columnconfigure(0, weight=1, minsize=225)
        self.grid_columnconfigure((1,2), weight=1, minsize=225)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        # Background Color Selectors
        self.background_bg_selector = ColorSelector(self, color_label="Background Color Mode:", default_color="white", apply_btn=False)
        self.background_bg_selector.grid(row=1, column=0, padx=(20, 0), pady=(0, 20), sticky="w")
        self.background_paper_selector = ColorSelector(self, color_label = "Paper Color Mode:", default_color="white", apply_btn=False)
        self.background_paper_selector.grid(row=1, column=1, padx=(25, 0), pady=(0, 20), sticky="w")


#################
# Font Selector #
#################
class FontSelector(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (3x3)
        self.grid_columnconfigure(0, weight=1, minsize=225)
        self.grid_columnconfigure((1,2), weight=1, minsize=150)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)

        # Available font families
        font_families = families()

        # Option variable for font selection
        self.select_font = tk.StringVar(value=font_families[0])

        # Label for font selection
        self.font_label = customtkinter.CTkLabel(self, text="Font Family:")
        self.font_label.grid(row=0, column=0, padx=(20,0), pady=(0,10), sticky="w")

        # Label for font selection
        self.font_optionmenu = customtkinter.CTkOptionMenu(self, variable=self.select_font, values=font_families)
        self.font_optionmenu.grid(row=1, column=0, padx=(20,0), pady=(0,20), sticky="w")

        # Label for font size selection
        self.size_label = customtkinter.CTkLabel(self, text="Font Size:")
        self.size_label.grid(row=0, column=1, padx=(35,0), pady=(0,10), sticky="w")

        # Entry for font size input
        self.size_entry = customtkinter.CTkEntry(self)
        self.size_entry.insert(0, "10")  # Set the default value to 10
        self.size_entry.grid(row=1, column=1, padx=(35,0), pady=(0,20), sticky="w")

        # Font Color Selection
        self.font_color_selector = ColorSelector(self, color_label="Font Color Mode:", apply_btn=False)
        self.font_color_selector.grid(row=0, column=2, rowspan=2,padx=(35,0), pady=(0,0), sticky="w")

########################
# General Config Frame #
########################
class GeneralConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(border_width=-2)

        # Grid settings (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

        # Configurations Tabs
        self.config_tabview = customtkinter.CTkTabview(self)
        self.config_tabview.add("Units")
        self.config_tabview.add("Background")
        self.config_tabview.add("Font")
        self.config_tabview.grid(row=0, column=0, padx=(20, 20), pady=(0, 20), sticky="nsew")

        # Units Tab
        self.units_selector = UnitsSelector(self.config_tabview.tab("Units"))
        self.units_selector.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Background Tab
        self.background_bg_selector = BackgroundSelector(self.config_tabview.tab("Background"))
        self.background_bg_selector.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="w")

        # Font Tab
        self.font_selector = FontSelector(self.config_tabview.tab("Font"))
        self.font_selector.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

#####################
# Node Config Frame #
#####################
class NodeConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (4x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text="Node Configuration")
        self.title_label.configure(font=("Helvetica", 12, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20,5))

        # Separator line
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Node thickness selection
        self.thickness_label = customtkinter.CTkLabel(self, text="Thickness:")
        self.thickness_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.thickness_var = tk.IntVar(value=20)
        self.thickness_entry = customtkinter.CTkEntry(self, validate="key", validatecommand=(self.register(self.validate_integer), "%P"))
        self.thickness_entry.configure(textvariable=self.thickness_var)
        self.thickness_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Node padding selection
        self.padding_label = customtkinter.CTkLabel(self, text="Pad:")
        self.padding_label.grid(row=3, column=0, padx=10, pady=(0,10), sticky="e")

        self.padding_var = tk.IntVar(value=15)
        self.padding_entry = customtkinter.CTkEntry(self, validate="key", validatecommand=(self.register(self.validate_integer), "%P"))
        self.padding_entry.configure(textvariable=self.padding_var)
        self.padding_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def validate_integer(self, value):
        try:
            if value:
                int(value)
            return True
        except ValueError:
            return False
        
#####################
# Link Config Frame #
#####################
class LinkConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Initializing variables
        self.sankey_data = None

        # Configuring the attributes of the frame
        self.configure(fg_color=master.cget('fg_color'), border_width=0)

        # Grid settings (4x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=3)

        # Title label
        self.title_label = customtkinter.CTkLabel(self, text="Border Configuration")
        self.title_label.configure(font=("Helvetica", 12, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(15,5))

        # Separator line
        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Link width selection
        self.width_label = customtkinter.CTkLabel(self, text="Width:")
        self.width_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.width_var = tk.IntVar(value=0.5)
        self.width_entry = customtkinter.CTkEntry(self, validate="key")
        self.width_entry.configure(textvariable=self.width_var)
        self.width_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Link Color Selection
        self.line_color_selector = ColorSelector(self, color_label="Line Color Mode:", apply_btn=False)
        self.line_color_selector.grid(row=3, column=0, columnspan=2,padx=(10,0), pady=(5,0), sticky="w")

######################
# Graph Config Frame #
######################
class GraphConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Configuring the attributes of the frame
        self.configure(border_width=-2)

        # Grid settings (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((2,3), weight=2)

        # Node Configuration
        self.node_config_frame = NodeConfigFrame(self)
        self.node_config_frame.grid(row=0, column=0, padx=(0, 20), pady=(0, 0), sticky="nsew")

        # Link Configuration
        self.link_config_frame = LinkConfigFrame(self)
        self.link_config_frame.grid(row=1, column=0, padx=(0, 20), pady=(0, 0), sticky="nsew")

#######
# App #
#######
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # App title
        self.title("Graphing Tool")

        # Initializing variables
        self.sankey_data = None

        ## Window settings
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Set window size (optional, to make the window a bit smaller than the screen size)
        window_width = screen_width * 0.82
        window_height = screen_height * 0.80
        # Set window position (optional, to center the window)
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        # Set window geometry
        self.geometry(f'{int(window_width)}x{int(window_height)}+{position_right}+{position_top}')

        # Grid settings (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1, minsize=730)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0,1,2), weight=1)

        # Sidebar
        self.sidebar_frame = Sidebar(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Description Frame
        self.description_frame = Description_Frame(self, width=100)
        self.description_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # General Config Frame
        self.general_config_frame = GeneralConfigFrame(self)
        self.general_config_frame.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Graph Config Frame
        self.graph_config_frame = GraphConfigFrame(self)
        self.graph_config_frame.grid(row=0, column=2, rowspan=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Plot Title Entry
        self.plot_title_entry = customtkinter.CTkEntry(self, placeholder_text="Enter the Plot Title")
        self.plot_title_entry.grid(row=3, column=1, columnspan=1, padx=(0, 0), pady=(20, 20), sticky="nsew")

        # Plot Button
        self.plot_button = customtkinter.CTkButton(self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Plot Graph", command=self.generate_graph)
        self.plot_button.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")


    # Generate Sankey Diagram Function
    def generate_graph(self):
        
        if self.sankey_data is None:
            print("Please load all data before plotting.")
            return

        # Retrieve the values from the input widgets
        plot_title = self.plot_title_entry.get()
        selected_unit = self.general_config_frame.units_selector.selected_unit.get()
        font_family = self.general_config_frame.font_selector.select_font.get()
        font_size = int(self.general_config_frame.font_selector.size_entry.get())
        node_thickness = int(self.graph_config_frame.node_config_frame.thickness_var.get())
        node_padding = int(self.graph_config_frame.node_config_frame.padding_var.get())
        link_width = int(self.graph_config_frame.link_config_frame.width_var.get())

         # Retrieve the colors
        bg_color = self.general_config_frame.background_bg_selector.background_bg_selector.color_variable.get()
        paper_color = self.general_config_frame.background_bg_selector.background_paper_selector.color_variable.get()
        font_color = self.general_config_frame.font_selector.font_color_selector.color_variable.get()
        line_color = self.graph_config_frame.link_config_frame.line_color_selector.color_variable.get()

        # Loading the variables for the Sankey Diagram
        sankey_data = self.sankey_data.copy()
        node_labels = sankey_data['node_labels']
        node_colors = sankey_data['node_colors']
        link_sources = sankey_data['link_sources']
        link_targets = sankey_data['link_targets']
        link_values = sankey_data['link_values']
        link_colors = sankey_data['link_colors']
        link_labels = sankey_data['link_labels']

        # Creating the Sankey Diagram
        figure= create_sankey_diagram(link_sources, link_targets, link_values, node_labels, link_labels, node_colors, link_colors,
                                      node_pad=node_padding, node_thickness=node_thickness, line_color=line_color, line_width=link_width,
                                      font_size=font_size, font_color=font_color, font_family=font_family,
                                      plot_bgcolor=bg_color, paper_bgcolor=paper_color,
                                      plot_title = plot_title, units = selected_unit)
        # Saving the figure to html and plottig it in the web browser
        temp_html = os.path.join(tempfile.gettempdir(), "temp.html")
        figure.write_html(temp_html)
        webbrowser.open_new_tab('file://' + os.path.realpath(temp_html))
    

app = App()
app.mainloop() 

    