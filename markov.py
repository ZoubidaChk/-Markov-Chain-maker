import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


class MarkovChainCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculateur de Chaîne de Markov - par Zoubida")
        self.root.geometry("1000x750")
        self.root.configure(bg="#d1fae5")

        self.nb_states = 3
        self.matrix_entries = []
        self.dist_entries = []

        self.create_ui()
        self.update_matrix_grid()

    def create_ui(self):
        header_frame = tk.Frame(self.root, bg="#059669", height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Calculateur de Chaîne de Markov",
            font=("Arial", 18, "bold"),
            bg="#059669",
            fg="white"
        ).pack(pady=(12, 3))

        tk.Label(
            header_frame,
            text="Développé par Zoubida",
            font=("Arial", 12),
            bg="#059669",
            fg="#d1fae5"
        ).pack()

        main_container = tk.Frame(self.root, bg="#d1fae5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_panel = tk.Frame(main_container, bg="#d1fae5")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_panel = tk.Frame(main_container, bg="#d1fae5")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_section_label(left_panel, "1. Nombre d'états (Nb)")
        nb_frame = tk.Frame(left_panel, bg="white", bd=2, relief=tk.RAISED)
        nb_frame.pack(fill=tk.X)

        self.nb_spinbox = tk.Spinbox(
            nb_frame, from_=1, to=10, width=15,
            font=("Arial", 11), command=self.update_matrix_grid
        )
        self.nb_spinbox.delete(0, tk.END)
        self.nb_spinbox.insert(0, "3")
        self.nb_spinbox.pack(pady=8)

        self.create_section_label(left_panel, "2. Matrice de transition P")
        self.matrix_frame = tk.Frame(left_panel, bg="white", bd=2, relief=tk.RAISED)
        self.matrix_frame.pack(fill=tk.BOTH, expand=True)

        # Button frame for Random Matrix and Graph buttons
        button_frame = tk.Frame(left_panel, bg="#d1fae5")
        button_frame.pack(fill=tk.X, pady=(6, 0))

        # Random Matrix Button
        tk.Button(
            button_frame,
            text="Matrice Aléatoire",
            command=self.generate_random_matrix,
            bg="#0891b2",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=6,
            cursor="hand2"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))

        # Graph Button
        tk.Button(
            button_frame,
            text="Afficher le Graphe",
            command=self.show_graph,
            bg="#7c3aed",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=6,
            cursor="hand2"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))

        # Calculate Button
        tk.Button(
            left_panel,
            text="Calculer",
            command=self.calculate,
            bg="#10b981",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=8,
            cursor="hand2"
        ).pack(fill=tk.X, pady=(6, 10))

        self.create_section_label(left_panel, "3. Instant t (≥ 0)")
        t_frame = tk.Frame(left_panel, bg="white", bd=2, relief=tk.RAISED)
        t_frame.pack(fill=tk.X)

        self.t_spinbox = tk.Spinbox(t_frame, from_=0, to=100, width=15, font=("Arial", 11))
        self.t_spinbox.insert(0, "0")
        self.t_spinbox.pack(pady=8)

        self.create_section_label(left_panel, "4. Distribution π(t)")
        self.dist_frame = tk.Frame(left_panel, bg="white", bd=2, relief=tk.RAISED)
        self.dist_frame.pack(fill=tk.X)

        self.create_section_label(left_panel, "5. Instant k (> t)")
        k_frame = tk.Frame(left_panel, bg="white", bd=2, relief=tk.RAISED)
        k_frame.pack(fill=tk.X)

        self.k_spinbox = tk.Spinbox(k_frame, from_=1, to=100, width=15, font=("Arial", 11))
        self.k_spinbox.insert(0, "5")
        self.k_spinbox.pack(pady=8)

        # MAIN CALCULATE BUTTON
        tk.Button(
            left_panel,
            text="Calculer π(k) = π(t) × P^(k−t)",
            command=self.calculate,
            bg="#059669",
            fg="white",
            font=("Arial", 13, "bold"),
            pady=12,
            cursor="hand2"
        ).pack(fill=tk.X, pady=10)

        tk.Label(
            right_panel,
            text="Résultats",
            font=("Arial", 15, "bold"),
            bg="#d1fae5",
            fg="#047857"
        ).pack()

        self.result_text = scrolledtext.ScrolledText(
            right_panel,
            font=("Courier", 10),
            bg="#f0fdf4",
            fg="#065f46"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert("1.0", "Remplissez les paramètres puis cliquez sur Calculer.")
        self.result_text.config(state=tk.DISABLED)

    def create_section_label(self, parent, text):
        tk.Label(
            parent, text=text, anchor=tk.W,
            font=("Arial", 10, "bold"),
            bg="#d1fae5", fg="#047857"
        ).pack(fill=tk.X, pady=(8, 4))

    def update_matrix_grid(self):
        for w in self.matrix_frame.winfo_children():
            w.destroy()
        for w in self.dist_frame.winfo_children():
            w.destroy()

        self.nb_states = int(self.nb_spinbox.get())
        n = self.nb_states
        self.matrix_entries = []
        self.dist_entries = []

        for i in range(n):
            row = []
            row_frame = tk.Frame(self.matrix_frame, bg="white")
            row_frame.pack()
            for j in range(n):
                e = tk.Entry(row_frame, width=8, justify=tk.CENTER)
                e.insert(0, f"{1/n:.3f}")
                e.pack(side=tk.LEFT, padx=2)
                row.append(e)
            self.matrix_entries.append(row)

        for i in range(n):
            e = tk.Entry(self.dist_frame, width=8, justify=tk.CENTER)
            e.insert(0, f"{1/n:.3f}")
            e.pack(side=tk.LEFT, padx=5, pady=10)
            self.dist_entries.append(e)

    def generate_random_matrix(self):
        """Generate a random stochastic matrix"""
        n = self.nb_states
        # Generate random values
        random_matrix = np.random.rand(n, n)
        # Normalize each row to sum to 1
        random_matrix = random_matrix / random_matrix.sum(axis=1, keepdims=True)
        
        # Update the matrix entries
        for i in range(n):
            for j in range(n):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, f"{random_matrix[i][j]:.3f}")
        
        messagebox.showinfo("Succès", "Matrice aléatoire générée avec succès!")

    def show_graph(self):
        """Display the Markov chain as a directed graph"""
        try:
            n = self.nb_states
            P = np.array([[float(e.get()) for e in row] for row in self.matrix_entries])
            
            if np.any(P < 0):
                raise ValueError("Les probabilités doivent être ≥ 0")
            
            # Create a new window for the graph
            graph_window = tk.Toplevel(self.root)
            graph_window.title("Graphe de la Chaîne de Markov")
            graph_window.geometry("800x600")
            graph_window.configure(bg="white")
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Position nodes in a circle
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
            pos = {i: (np.cos(angles[i]), np.sin(angles[i])) for i in range(n)}
            
            # Draw nodes
            for i in range(n):
                x, y = pos[i]
                circle = plt.Circle((x, y), 0.15, color='#059669', ec='#047857', linewidth=2, zorder=3)
                ax.add_patch(circle)
                ax.text(x, y, f'S{i}', ha='center', va='center', 
                       fontsize=14, fontweight='bold', color='white', zorder=4)
            
            # Draw edges (transitions)
            for i in range(n):
                for j in range(n):
                    prob = P[i][j]
                    if prob > 0.01:  # Only show transitions with probability > 1%
                        x1, y1 = pos[i]
                        x2, y2 = pos[j]
                        
                        if i == j:
                            # Self-loop
                            loop_offset = 0.3
                            angle = angles[i]
                            loop_x = x1 + loop_offset * np.cos(angle)
                            loop_y = y1 + loop_offset * np.sin(angle)
                            
                            circle = plt.Circle((loop_x, loop_y), 0.15, 
                                              fill=False, ec='#0891b2', linewidth=2, zorder=2)
                            ax.add_patch(circle)
                            
                            # Label for self-loop
                            label_x = x1 + (loop_offset + 0.2) * np.cos(angle)
                            label_y = y1 + (loop_offset + 0.2) * np.sin(angle)
                            ax.text(label_x, label_y, f'{prob:.2f}', 
                                   ha='center', va='center', fontsize=9,
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                           edgecolor='#0891b2', linewidth=1.5), zorder=5)
                        else:
                            # Regular edge
                            # Offset for curved arrows
                            dx = x2 - x1
                            dy = y2 - y1
                            dist = np.sqrt(dx**2 + dy**2)
                            
                            # Shorten arrow to not overlap with nodes
                            offset = 0.15
                            x1_adj = x1 + (dx/dist) * offset
                            y1_adj = y1 + (dy/dist) * offset
                            x2_adj = x2 - (dx/dist) * offset
                            y2_adj = y2 - (dy/dist) * offset
                            
                            # Draw arrow with curve
                            ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                                      arrowprops=dict(arrowstyle='->', lw=2, color='#0891b2',
                                                    connectionstyle="arc3,rad=0.2", zorder=2))
                            
                            # Label position (middle of edge)
                            mid_x = (x1 + x2) / 2
                            mid_y = (y1 + y2) / 2
                            # Offset label perpendicular to edge
                            perp_x = -dy / dist * 0.15
                            perp_y = dx / dist * 0.15
                            
                            ax.text(mid_x + perp_x, mid_y + perp_y, f'{prob:.2f}',
                                   ha='center', va='center', fontsize=9,
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                           edgecolor='#0891b2', linewidth=1.5), zorder=5)
            
            ax.set_xlim(-1.8, 1.8)
            ax.set_ylim(-1.8, 1.8)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title('Graphe de la Chaîne de Markov\n(Les probabilités < 0.01 sont masquées)', 
                        fontsize=14, fontweight='bold', color='#047857', pad=20)
            
            # Embed the plot in tkinter window
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher le graphe:\n{str(e)}")

    def calculate(self):
        try:
            n = self.nb_states
            P = np.array([[float(e.get()) for e in row] for row in self.matrix_entries])
            pi = np.array([float(e.get()) for e in self.dist_entries])
            if np.any(P < 0) or np.any(pi < 0):
                raise ValueError("Les probabilités doivent être ≥ 0")
            if not np.allclose(P.sum(axis=1), 1, atol=1e-2):
                raise ValueError("Chaque ligne de P doit sommer à 1")
            if not np.isclose(pi.sum(), 1, atol=1e-2):
                raise ValueError("La distribution π(t) doit sommer à 1")

            t = int(self.t_spinbox.get())
            k = int(self.k_spinbox.get())
            if k <= t:
                raise ValueError("k doit être strictement supérieur à t")

            Pk = np.linalg.matrix_power(P, k - t)
            pik = pi @ Pk

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"π({k}) = {pik}")
            self.result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovChainCalculator(root)
    root.mainloop()