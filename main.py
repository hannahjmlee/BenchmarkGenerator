import tkinter as tk
import numpy as np
from filewriter import *

class MapfBenchmarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MAPF Benchmark Creator")

        # Default grid size
        self.rows = 10
        self.cols = 10
        self.cell_size = 50  # Size of each cell in pixels

        # Create UI for setting grid size
        self.create_size_controls()

        # Create the grid
        self.create_grid()

    def create_size_controls(self):
        control_frame = tk.Frame(self)
        control_frame.grid(row=0, column=0, pady=10, sticky="w")

        # Row size input
        row_label = tk.Label(control_frame, text="Rows:")
        row_label.grid(row=0, column=0, sticky="e")
        self.row_entry = tk.Entry(control_frame, width=5)
        self.row_entry.grid(row=0, column=1)
        self.row_entry.insert(0, str(self.rows))

        # Column size input
        col_label = tk.Label(control_frame, text="Columns:")
        col_label.grid(row=1, column=0, sticky="e")
        self.col_entry = tk.Entry(control_frame, width=5)
        self.col_entry.grid(row=1, column=1)
        self.col_entry.insert(0, str(self.cols))

        # Button to update grid size
        set_size_button = tk.Button(control_frame, text="Set Grid Size", command=self.update_grid_size)
        set_size_button.grid(row=2, column=0, columnspan=2)

        # Name entry for the environment file
        name_label = tk.Label(control_frame, text="Env Name:")
        name_label.grid(row=0, column=2, sticky="e", padx=(20, 0))
        self.name_entry = tk.Entry(control_frame, width=15)
        self.name_entry.grid(row=0, column=3)

        # Button to generate the environment array
        generate_button = tk.Button(control_frame, text="Generate Environment", command=self.generate_environment)
        generate_button.grid(row=1, column=2, columnspan=2, pady=(5, 0), padx=(20,0))

        # Number of scenarios input
        scenario_label = tk.Label(control_frame, text="Num Scenarios:")
        scenario_label.grid(row=0, column=4, sticky="e", padx=(20, 0))
        self.scenario_entry = tk.Entry(control_frame, width=5)
        self.scenario_entry.grid(row=0, column=5)
        self.scenario_entry.insert(0, "1")

        # Button to generate random scenarios
        random_scenario_button = tk.Button(control_frame, text="Generate Scenarios", command=self.generate_random_scenario)
        random_scenario_button.grid(row=1, column=4, columnspan=2, pady=(5, 0), padx=(20, 0))

    def create_grid(self):
        # Create a frame to hold the grid
        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.cells = {}
        for row in range(self.rows):
            for col in range(self.cols):
                btn = tk.Button(self.grid_frame, bg="white", relief="raised")
                btn.grid(row=row, column=col, sticky="nsew")
                self.cells[(row, col)] = btn

                # Bind mouse events to handle dragging
                btn.bind("<Button-1>", self.on_drag_start)
                btn.bind("<B1-Motion>", self.on_drag)
                btn.bind("<ButtonRelease-1>", self.on_drag_end)

        # Ensure all rows and columns have the same size to maintain square cells
        for row in range(self.rows):
            self.grid_frame.grid_rowconfigure(row, minsize=self.cell_size)
        for col in range(self.cols):
            self.grid_frame.grid_columnconfigure(col, minsize=self.cell_size)

    def on_drag_start(self, event):
        # Start the drag operation by determining the initial color and toggling the first cell
        widget = event.widget
        self.initial_color = "white" if widget.cget("bg") == "black" else "black"
        self.toggle_cell(widget)
        self.dragging = True

    def on_drag(self, event):
        # Get the widget directly under the mouse pointer
        widget = event.widget.winfo_containing(event.x_root, event.y_root)

        if widget and widget in self.cells.values():
            # Set all dragged-over cells to the initial opposite color
            widget.config(bg=self.initial_color)

    def toggle_cell(self, widget):
        # Toggle the cell color between black and white
        current_color = widget.cget("bg")
        new_color = "white" if current_color == "black" else "black"
        widget.config(bg=new_color)


    def on_drag_end(self, event):
        # End the drag operation
        self.dragging = False

    def on_click(self, row, col):
        btn = self.cells[(row, col)]
        current_color = btn.cget("bg")
        new_color = "black" if current_color == "white" else "white"
        btn.config(bg=new_color)

    def update_grid_size(self):
        # Clear the existing grid
        self.grid_frame.destroy()

        # Get the new grid size from the entries
        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())
        except ValueError:
            # If input is not a valid integer, do nothing
            return

        # Adjust cell size based on grid size (scale down as grid size increases)
        max_size = max(self.rows, self.cols)
        self.cell_size = max(10, 500 // max_size)  # Minimum cell size set to 10 pixels

        # Recreate the grid with the new size
        self.create_grid()

    def generate_environment(self):
        # Create a numpy array to store the environment
        self.np_environment = np.zeros((self.rows, self.cols), dtype=bool)

        for row in range(self.rows):
            for col in range(self.cols):
                cell_color = self.cells[(row, col)].cget("bg")
                self.np_environment[row, col] = True if cell_color == "white" else False

        # Get the environment name from the text entry
        self.env_name = self.name_entry.get()
        if not self.env_name:
            self.env_name = "environment"  # Default name if none is provided

        # Save the environment array to a file
        generate_text_file(self.np_environment, f"{self.env_name}.map")
        print(f"Environment {self.env_name}.map created.")

    def generate_random_scenario(self):
    # Save the number of scenarios from the text box
        try:
            self.num_scenarios = int(self.scenario_entry.get())
        except ValueError:
            self.num_scenarios = 1  # Default to 1 if the input is not valid

        map_name = f"{self.env_name}.map"
        for i in range(self.num_scenarios): 
            scenario_file = f"{self.name_entry.get()}-random-{i + 1}.scen"
            generate_scenario_file(self.np_environment, map_name, scenario_file)
            print(f"Scenario {scenario_file} created. ")
            


    

if __name__ == "__main__":
    app = MapfBenchmarkApp()
    app.mainloop()



