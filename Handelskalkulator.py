import tkinter as tk
from tkinter import ttk, messagebox
import json

# --- Kalkulationsfunktionen ---
def vorwaertskalkulation(listeneinkaufspreis, lieferrabatt_satz, lieferskonto_satz,
                         bezugskosten, handlungskostenzuschlag_satz, gewinnzuschlag_satz,
                         kundenkonto_satz, vertreterprovision_satz,
                         kundenrabatt_satz, umsatzsteuer_satz):

    zieleinkaufspreis = listeneinkaufspreis * (1 - lieferrabatt_satz)
    bareinkaufspreis = zieleinkaufspreis * (1 - lieferskonto_satz)
    bezugspreis = bareinkaufspreis + bezugskosten
    selbstkosten = bezugspreis * (1 + handlungskostenzuschlag_satz)
    barverkaufspreis = selbstkosten * (1 + gewinnzuschlag_satz)
    zielverkaufspreis = barverkaufspreis / (1 - kundenkonto_satz - vertreterprovision_satz)
    nettoverkaufspreis = zielverkaufspreis / (1 - kundenrabatt_satz)
    bruttoverkaufspreis = nettoverkaufspreis * (1 + umsatzsteuer_satz)

    return {
        "Listeneinkaufspreis": listeneinkaufspreis,
        "Zieleinkaufspreis": zieleinkaufspreis,
        "Bareinkaufspreis": bareinkaufspreis,
        "Bezugspreis": bezugspreis,
        "Selbstkosten": selbstkosten,
        "Barverkaufspreis": barverkaufspreis,
        "Zielverkaufspreis": zielverkaufspreis,
        "Nettoverkaufspreis": nettoverkaufspreis,
        "Bruttoverkaufspreis": bruttoverkaufspreis
    }

def rueckwaertskalkulation(bruttoverkaufspreis, umsatzsteuer_satz, kundenrabatt_satz,
                           kundenkonto_satz, vertreterprovision_satz,
                           gewinnzuschlag_satz, handlungskostenzuschlag_satz,
                           bezugskosten, lieferskonto_satz, lieferrabatt_satz):

    nettoverkaufspreis = bruttoverkaufspreis / (1 + umsatzsteuer_satz)
    zielverkaufspreis = nettoverkaufspreis * (1 - kundenrabatt_satz)
    barverkaufspreis = zielverkaufspreis * (1 - kundenkonto_satz - vertreterprovision_satz)
    selbstkosten = barverkaufspreis / (1 + gewinnzuschlag_satz)
    bezugspreis = selbstkosten / (1 + handlungskostenzuschlag_satz)
    bareinkaufspreis = bezugspreis - bezugskosten
    zieleinkaufspreis = bareinkaufspreis / (1 - lieferskonto_satz)
    listeneinkaufspreis = zieleinkaufspreis / (1 - lieferrabatt_satz)

    return {
        "Bruttoverkaufspreis": bruttoverkaufspreis,
        "Nettoverkaufspreis": nettoverkaufspreis,
        "Zielverkaufspreis": zielverkaufspreis,
        "Barverkaufspreis": barverkaufspreis,
        "Selbstkosten": selbstkosten,
        "Bezugspreis": bezugspreis,
        "Bareinkaufspreis": bareinkaufspreis,
        "Zieleinkaufspreis": zieleinkaufspreis,
        "Listeneinkaufspreis": listeneinkaufspreis
    }

# --- GUI-Logik ---
class HandelsrechnerApp:
    def __init__(self, master):
        self.master = master
        master.title("DENNIS NOLDEN Handelskalkulator")
        master.geometry("600x800")
        master.resizable(False, False)
        master.configure(bg="#1a1a2e")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background="#1a1a2e", foreground="#e0e0e0")
        self.style.configure('TLabel', background="#1a1a2e", foreground="#00bfff", font=('Arial', 10))
        self.style.configure('TButton', background="#ff4500", foreground="#ffffff", font=('Arial', 10, 'bold'), borderwidth=0)
        self.style.map('TButton', background=[('active', '#ff6347')])
        self.style.configure('TRadiobutton', background="#1a1a2e", foreground="#e0e0e0", indicatoron=0, relief="flat", padding=5)
        self.style.map('TRadiobutton', background=[('active', '#33334d'), ('selected', '#00bfff')])
        self.style.map('TRadiobutton', foreground=[('selected', '#ffffff')])
        
        self.style.configure('TEntry', fieldbackground="#33334d", foreground="#ffffff", relief="flat")
        self.style.map('TEntry', fieldbackground=[('focus', '#4a4a6d')])

        # Header Frame
        header_frame = ttk.Frame(master)
        header_frame.pack(pady=10)
        ttk.Label(header_frame, text="DENNIS NOLDEN", font=('Arial', 18, 'bold'), foreground="#ff4500").pack(side=tk.LEFT, padx=10)
        ttk.Label(header_frame, text="Handelskalkulator", font=('Arial', 18, 'bold'), foreground="#00bfff").pack(side=tk.LEFT)

        # Auswahl der Kalkulationsrichtung
        self.modus_var = tk.StringVar(value="vorwaerts")
        modus_frame = ttk.Frame(master)
        modus_frame.pack(pady=10)
        ttk.Radiobutton(modus_frame, text="Vorwärtskalkulation", variable=self.modus_var, value="vorwaerts",
                        command=self.toggle_inputs, style='TRadiobutton').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(modus_frame, text="Rückwärtskalkulation", variable=self.modus_var, value="rueckwaerts",
                        command=self.toggle_inputs, style='TRadiobutton').pack(side=tk.LEFT, padx=5)

        # Container für die Eingabefelder
        self.input_container_frame = ttk.Frame(master)
        self.input_container_frame.pack(padx=20, pady=5)
        
        # Erstelle alle Widgets und verwalte sie in einer flachen Liste
        self.widgets = self.create_all_widgets(self.input_container_frame)

        # Berechnen Button
        self.calculate_button = ttk.Button(master, text="Berechnen", command=self.calculate, style='TButton')
        self.calculate_button.pack(pady=10)

        # Ergebnisbereich
        self.result_label = ttk.Label(master, text="Ergebnisse", font=('Arial', 12, 'bold'), foreground="#00bfff", background="#1a1a2e")
        self.result_label.pack(pady=(0, 5))
        
        self.result_text = tk.Text(master, height=15, width=60, bg="#33334d", fg="#ffffff", font=('Arial', 10), relief="flat")
        self.result_text.pack(padx=20, pady=5)

        self.toggle_inputs()

    def create_all_widgets(self, master):
        widgets = []
        vorwaerts_fields = [
            ("Listeneinkaufspreis", "listeneinkaufspreis"), ("Lieferrabatt (%)", "lieferrabatt_satz"),
            ("Lieferskonto (%)", "lieferskonto_satz"), ("Bezugskosten", "bezugskosten"),
            ("Handlungskostenzuschlag (%)", "handlungskostenzuschlag_satz"),
            ("Gewinnzuschlag (%)", "gewinnzuschlag_satz"), ("Kundenkonto (%)", "kundenkonto_satz"),
            ("Vertreterprovision (%)", "vertreterprovision_satz"), ("Kundenrabatt (%)", "kundenrabatt_satz"),
            ("Umsatzsteuer (%)", "umsatzsteuer_satz"),
        ]
        rueckwaerts_fields = [
            ("Bruttoverkaufspreis", "bruttoverkaufspreis"), ("Umsatzsteuer (%)", "umsatzsteuer_satz_r"),
            ("Kundenrabatt (%)", "kundenrabatt_satz_r"), ("Kundenkonto (%)", "kundenkonto_satz_r"),
            ("Vertreterprovision (%)", "vertreterprovision_satz_r"), ("Gewinnzuschlag (%)", "gewinnzuschlag_satz_r"),
            ("Handlungskostenzuschlag (%)", "handlungskostenzuschlag_satz_r"),
            ("Bezugskosten", "bezugskosten_r"), ("Lieferskonto (%)", "lieferskonto_satz_r"),
            ("Lieferrabatt (%)", "lieferrabatt_satz_r"),
        ]
        
        # Erstelle Vorwärts-Widgets
        for label_text, var_name in vorwaerts_fields:
            lbl = ttk.Label(master, text=f"{label_text}:")
            entry = ttk.Entry(master)
            widgets.append({'type': 'vorwaerts', 'label': lbl, 'entry': entry, 'var_name': var_name, 'label_text': label_text})

        # Erstelle Rückwärts-Widgets
        for label_text, var_name in rueckwaerts_fields:
            lbl = ttk.Label(master, text=f"{label_text}:")
            entry = ttk.Entry(master)
            widgets.append({'type': 'rueckwaerts', 'label': lbl, 'entry': entry, 'var_name': var_name, 'label_text': label_text})

        return widgets

    def toggle_inputs(self):
        # Alle Widgets ausblenden
        for widget in self.widgets:
            widget['label'].grid_remove()
            widget['entry'].grid_remove()

        # Nur die Widgets des ausgewählten Modus anzeigen
        mode = self.modus_var.get()
        row = 0
        for widget in self.widgets:
            if widget['type'] == mode:
                widget['label'].grid(row=row, column=0, sticky="w", padx=5, pady=2)
                widget['entry'].grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                row += 1
        
        self.result_text.delete('1.0', tk.END)

    def get_value_from_entry(self, entry_data):
        try:
            val = float(entry_data['entry'].get())
            if "satz" in entry_data['var_name']:
                return val / 100
            return val
        except ValueError:
            raise ValueError(entry_data['label_text'])

    def calculate(self):
        self.result_text.delete('1.0', tk.END)
        try:
            modus = self.modus_var.get()
            
            if modus == "vorwaerts":
                inputs = {widget['var_name']: self.get_value_from_entry(widget) for widget in self.widgets if widget['type'] == 'vorwaerts'}
                ergebnis = vorwaertskalkulation(**inputs)
            
            elif modus == "rueckwaerts":
                inputs = {widget['var_name']: self.get_value_from_entry(widget) for widget in self.widgets if widget['type'] == 'rueckwaerts'}
                ergebnis = rueckwaertskalkulation(
                    bruttoverkaufspreis=inputs['bruttoverkaufspreis'],
                    umsatzsteuer_satz=inputs['umsatzsteuer_satz_r'],
                    kundenrabatt_satz=inputs['kundenrabatt_satz_r'],
                    kundenkonto_satz=inputs['kundenkonto_satz_r'],
                    vertreterprovision_satz=inputs['vertreterprovision_satz_r'],
                    gewinnzuschlag_satz=inputs['gewinnzuschlag_satz_r'],
                    handlungskostenzuschlag_satz=inputs['handlungskostenzuschlag_satz_r'],
                    bezugskosten=inputs['bezugskosten_r'],
                    lieferskonto_satz=inputs['lieferskonto_satz_r'],
                    lieferrabatt_satz=inputs['lieferrabatt_satz_r']
                )

            # Ausgabe in das Textfeld
            formatted_result = json.dumps(ergebnis, indent=4)
            self.result_text.insert(tk.END, formatted_result)

        except ValueError as e:
            messagebox.showerror("Eingabefehler", f"Ungültige Eingabe für das Feld: '{e}'. Bitte geben Sie eine Zahl ein.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Es ist ein unerwarteter Fehler aufgetreten: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HandelsrechnerApp(root)
    root.mainloop()