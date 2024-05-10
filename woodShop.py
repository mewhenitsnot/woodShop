import tkinter as tk
from tkinter import messagebox

class WoodStoreApp:
    def __init__(self, master):
        """
        Initialize the Wood Store App.

        Args:
            master: Tkinter root window.
        """
        self.master = master
        master.title("Wood Store")
        master.geometry("400x300")

        # Buttons for various actions
        self.sell_button = tk.Button(master, text="Sell Wood", command=self.sell_wood, width=15, height=2)
        self.sell_button.place(relx=0.3, rely=0.4, anchor="center")

        self.view_button = tk.Button(master, text="View Orders", command=self.view_orders, width=15, height=2)
        self.view_button.place(relx=0.7, rely=0.4, anchor="center")

        self.revenue_button = tk.Button(master, text="Revenue", command=self.show_revenue, width=15, height=2)
        self.revenue_button.place(relx=0.5, rely=0.6, anchor="center")

        # Initialize orders list and total revenue
        self.orders = []
        self.total_revenue = 0

    def show_revenue(self):
        """
        Display the revenue details.
        """
        revenue_window = tk.Toplevel(self.master)
        revenue_window.title("Revenue Details")
        revenue_window.geometry("300x400")

        # Display individual order revenues
        scrollbar = tk.Scrollbar(revenue_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(revenue_window, yscrollcommand=scrollbar.set)
        for order in self.orders:
            listbox.insert(tk.END, f"Order Revenue: ${order['Price']:.2f}")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Display total revenue
        total_label = tk.Label(revenue_window, text=f"Total Revenue: ${self.total_revenue:.2f}", bg='lightblue', relief=tk.RAISED)
        total_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_revenue(self):
        """
        Update the total revenue based on orders.
        """
        self.total_revenue = sum(order['Price'] for order in self.orders)

    def sell_wood(self):
        """
        Open the window to sell wood.
        """
        sell_window = tk.Toplevel(self.master)
        sell_window.title("Sell Wood")
        sell_window.geometry("400x400")
        SellWood(sell_window, self.orders)

    def view_orders(self):
        """
        Open the window to view orders.
        """
        orders_window = tk.Toplevel(self.master)
        orders_window.title("View Orders")
        screen_width = orders_window.winfo_screenwidth()
        screen_height = orders_window.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        orders_window.geometry(f"{window_width}x{window_height}")
        ViewOrders(orders_window, self.orders, window_width, window_height)

class SellWood:
    def __init__(self, master, orders):
        """
        Initialize the Sell Wood window.

        Args:
            master: Tkinter root window.
            orders: List of orders.
        """
        self.master = master
        self.orders = orders
        self.current_order = {'planks': [], 'Price': 0}
        master.title("Sell Wood")
        master.geometry("300x250")

        # Dictionary to store plank sizes and dimensions
        self.sizes = {
            '2x4': {'Length': 8, 'Width': 0.33},
            '2x6': {'Length': 8, 'Width': 0.5},
            # Add more plank sizes as needed
        }

        # Dropdown for selecting plank size
        self.size_var = tk.StringVar(master)
        self.size_var.set('Select Size')
        self.size_menu = tk.OptionMenu(master, self.size_var, *self.sizes.keys())
        self.size_menu.grid(row=0, column=1, padx=10, pady=5)

        # Dropdown for selecting quantity
        self.quantity_var = tk.IntVar(master)
        self.quantity_var.set(1)
        self.quantity_menu = tk.OptionMenu(master, self.quantity_var, *(range(1, 11)))
        self.quantity_menu.grid(row=1, column=1, padx=10, pady=5)

        # Entry for entering wood density
        self.density_label = tk.Label(master, text="Wood Density (kg/m^3):")
        self.density_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.density_entry = tk.Entry(master)
        self.density_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for adding, removing, and completing order
        self.add_plank_button = tk.Button(master, text="Add Plank", command=self.add_plank, width=15, height=2)
        self.add_plank_button.grid(row=3, column=0, padx=5, pady=10)

        self.remove_plank_button = tk.Button(master, text="Remove Plank", command=self.remove_plank, width=15, height=2)
        self.remove_plank_button.grid(row=3, column=1, padx=5, pady=10)

        self.complete_order_button = tk.Button(master, text="Complete Order", command=self.complete_order, width=15, height=2)
        self.complete_order_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    def add_plank(self):
        """
        Add a plank to the current order.
        """
        size_key = self.size_var.get()
        if size_key == 'Select Size':
            messagebox.showerror("Error", "Please select a size.")
            return

        try:
            quantity = self.quantity_var.get()
            density = float(self.density_entry.get())
            size = self.sizes[size_key]
            volume = size['Length'] * size['Width'] * (1 / 12)
            price_per_plank = density * volume * 10
            total_price = price_per_plank * quantity
            plank_details = {'Size': size_key, 'Density': density, 'Quantity': quantity, 'Price': total_price}
            self.current_order['planks'].append(plank_details)
            self.current_order['Price'] += total_price
            messagebox.showinfo("Success", f"Added {quantity}x {size_key} plank(s). Current total: ${self.current_order['Price']:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for density.")

    def remove_plank(self):
        """
        Remove the last added plank from the current order.
        """
        if self.current_order['planks']:
            removed_plank = self.current_order['planks'].pop()
            self.current_order['Price'] -= removed_plank['Price']
            messagebox.showinfo("Removed", f"Removed one {removed_plank['Size']} plank. New total: ${self.current_order['Price']:.2f}")
        else:
            messagebox.showerror("Error", "No planks to remove.")

    def complete_order(self):
        """
        Complete the current order and add it to the list of orders.
        """
        if self.current_order['planks']:
            self.orders.append(self.current_order)
            self.master.destroy()
            messagebox.showinfo("Order Completed", f"Final total: ${self.current_order['Price']:.2f}")
        else:
            messagebox.showerror("Error", "No planks in the order to complete.")

class ViewOrders:
    def __init__(self, master, orders, window_width, window_height):
        """
        Initialize the View Orders window.

        Args:
            master: Tkinter root window.
            orders: List of orders.
            window_width: Width of the window.
            window_height: Height of the window.
        """
        self.master = master
        self.orders = orders
        master.title("View Orders")
        master.geometry(f"{window_width}x{window_height}")

        # Label for orders list
        self.orders_label = tk.Label(master, text="Today's Orders:")
        self.orders_label.pack(padx=10, pady=10)

        # Listbox to display orders
        self.orders_listbox = tk.Listbox(master, width=60, height=10, selectmode=tk.SINGLE)
        self.orders_listbox.pack(padx=10, pady=5)
        self.refresh_orders_list()

        # Frame for controls
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(padx=10, pady=10)

        # Dropdown for selecting plank to edit/delete
        self.plank_var = tk.StringVar(master)
        self.plank_var.set('Select Plank')
        self.plank_menu = tk.OptionMenu(self.control_frame, self.plank_var, 'Select Plank')
        self.plank_menu.pack(side=tk.TOP, fill=tk.X)

        # Entry for editing density
        self.edit_density_label = tk.Label(self.control_frame, text="Edit Density (kg/m^3):")
        self.edit_density_label.pack(side=tk.TOP)
        self.edit_density_entry = tk.Entry(self.control_frame, width=20)
        self.edit_density_entry.pack(side=tk.TOP)

        # Buttons for saving changes and deleting plank
        self.save_changes_button = tk.Button(self.control_frame, text="Save Changes", command=self.save_changes, width=15, height=2, state=tk.DISABLED)
        self.save_changes_button.pack(side=tk.TOP, pady=5)

        self.delete_plank_button = tk.Button(self.control_frame, text="Delete Plank", command=self.delete_plank, width=15, height=2, state=tk.DISABLED)
        self.delete_plank_button.pack(side=tk.TOP, pady=5)

        # Event binding for listbox selection
        self.orders_listbox.bind('<<ListboxSelect>>', self.on_order_select)

    def refresh_orders_list(self):
        """
        Refresh the orders list in the listbox.
        """
        self.orders_listbox.delete(0, tk.END)
        for index, order in enumerate(self.orders):
            self.orders_listbox.insert(tk.END, f"Order {index+1}: Price - ${order['Price']:.2f}")

    def on_order_select(self, event=None):
        """
        Handle selection of order in the listbox.
        """
        selected_index = self.orders_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_order = self.orders[selected_index]
            plank_choices = [f"Plank {i+1}: {plank['Size']}" for i, plank in enumerate(selected_order['planks'])]
            self.plank_var.set('Select Plank')
            self.plank_menu['menu'].delete(0, 'end')
            for choice in plank_choices:
                self.plank_menu['menu'].add_command(label=choice, command=lambda ch=choice: self.select_plank(ch, selected_index))
            self.save_changes_button.config(state=tk.DISABLED)
            self.delete_plank_button.config(state=tk.DISABLED)
            self.edit_density_entry.delete(0, tk.END)

    def select_plank(self, choice, order_index):
        """
        Handle selection of plank in the dropdown menu.
        """
        self.selected_plank_index = int(choice.split()[1]) - 1
        self.selected_order_index = order_index
        self.save_changes_button.config(state=tk.NORMAL)
        self.delete_plank_button.config(state=tk.NORMAL)
        self.edit_density_entry.delete(0, tk.END)
        self.edit_density_entry.insert(0, self.orders[self.selected_order_index]['planks'][self.selected_plank_index]['Density'])

    def save_changes(self):
        """
        Save changes made to the plank's density.
        """
        if self.selected_order_index is not None and self.selected_plank_index is not None:
            try:
                new_density = float(self.edit_density_entry.get())
                plank = self.orders[self.selected_order_index]['planks'][self.selected_plank_index]
                plank['Density'] = new_density
                volume = plank['Length'] * plank['Width'] * (1 / 12)
                new_price = new_density * volume * 10
                plank['Price'] = new_price
                total_price = sum(plank['Price'] for plank in self.orders[self.selected_order_index]['planks'])
                self.orders[self.selected_order_index]['Price'] = total_price
                self.refresh_orders_list()
                messagebox.showinfo("Success", "Plank and order updated successfully.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for density.")

    def delete_plank(self):
        """
        Delete the selected plank from the order.
        """
        if self.selected_order_index is not None and self.selected_plank_index is not None:
            del self.orders[self.selected_order_index]['planks'][self.selected_plank_index]
            total_price = sum(plank['Price'] for plank in self.orders[self.selected_order_index]['planks'])
            self.orders[self.selected_order_index]['Price'] = total_price
            self.refresh_orders_list()
            self.save_changes_button.config(state=tk.DISABLED)
            self.delete_plank_button.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Plank deleted successfully.")


def main():
    root = tk.Tk()
    app = WoodStoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

