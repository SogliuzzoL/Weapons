import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)

JSON_FILE = 'weapons.json'

def load_data():
    if not os.path.exists(JSON_FILE):
        return {"pieces": {}, "armes": {}}
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    weapons_catalog = data.get('armes', {})
    prices_catalog = data.get('pieces', {})
    
    # Variables de sélection
    selected_weapon = None
    selected_piece = None
    calc_type = request.form.get('calc_type', 'weapon')  # 'weapon' ou 'piece'
    
    # Variables de calcul
    components_dynamic = {}
    margin_percent = float(request.form.get('margin', 50))
    piece_qty = int(request.form.get('piece_qty', 1))
    
    cost_price = 0.0
    selling_price = 0.0
    profit = 0.0

    if request.method == 'POST':
        # --- MODE 1 : CALCUL POUR UNE ARME COMPLÈTE ---
        if calc_type == 'weapon':
            selected_weapon = request.form.get('weapon')
            if selected_weapon and selected_weapon in weapons_catalog:
                recipe = weapons_catalog[selected_weapon]['composants']
                
                for comp_name, qty in recipe.items():
                    base_price = prices_catalog.get(comp_name, 0)
                    input_name = f"price_{comp_name}"
                    current_price = float(request.form.get(input_name, base_price))
                    
                    cost_price += qty * current_price
                    components_dynamic[comp_name] = {
                        "quantite": qty,
                        "prix_actuel": current_price
                    }
                
                selling_price = cost_price * (1 + margin_percent / 100)
                profit = selling_price - cost_price

        # --- MODE 2 : CALCUL POUR UNE PIÈCE À L'UNITÉ ---
        elif calc_type == 'piece':
            selected_piece = request.form.get('piece')
            if selected_piece and selected_piece in prices_catalog:
                base_price = prices_catalog[selected_piece]
                
                # Permet de modifier le prix d'achat de la pièce en direct
                input_name = f"single_price_{selected_piece}"
                current_price = float(request.form.get(input_name, base_price))
                
                cost_price = current_price * piece_qty
                selling_price = cost_price * (1 + margin_percent / 100)
                profit = selling_price - cost_price
                
                components_dynamic[selected_piece] = {
                    "quantite": piece_qty,
                    "prix_actuel": current_price
                }

    return render_template(
        'index.html',
        weapons=weapons_catalog,
        prices=prices_catalog,
        calc_type=calc_type,
        selected_weapon=selected_weapon,
        selected_piece=selected_piece,
        piece_qty=piece_qty,
        components_dynamic=components_dynamic,
        margin_percent=margin_percent,
        cost_price=round(cost_price, 2),
        selling_price=round(selling_price, 2),
        profit=round(profit, 2)
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)