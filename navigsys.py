from flask import Flask, render_template

# Initilize the flask app
app = Flask(__name__, static_folder='interface')

def create_graph():
    graph = {
        "AD" : {"LH": 1, "SGMH": 1, "CJ": 1, "GH": 1, "MC": 4},
        "B"  : {"KHS": 2, "PL": 5, "TSU": 6, "CPAC": 4},
        "CC" : {"TS": 5, "TTF": 6},
        "CPAC" : {"B": 4, "PL": 3, "H": 5, "MH": 2, "GC": 2},
        "CS" : {"E": 1, "GAS": 3, "ENPS": 4},
        "E" : {"CS": 1, "RG": 4, "SHCC": 4, "EC": 6},
        "DBH" : {"MH": 1, "MC": 1, "LH": 1, "GC": 2},
        "EC" : {"PL": 2, "H": 3, "E": 6}
        "ENPS" : {"CS": 4, "ESPS": 1},
        "ESPS" : {"ENPS": 1, "H": 7},
        "GAH" : {"UP": 1, "SCPS": 2, "TSU": 2},
        "GAS": {"CS": 3, "RG": 2, "RH": 1, "HRE": 1},
        "GC" : {"CPAC": 2, "DBH": 2, "MH": 2, "NPS": 2},
        "GF" : {"TS": 2, "AF": 1, "TSC": 2},
        "GH" : {"H": 2, "MH": 2, "AD": 1, "LH": 1, "CJ": 1},
        "H" : {"CPAC": 5, "EC": 3, "ESPS": 7, "GH": 2, "PL": 3, "MH": 3},
        "HRE": {"GAS": 1, "RH": 1},
        "KHS": {"B": 2, "SRC": 3, "TG": 1, "PL": 3, "SHCC": 2},
        "LH" : {"AD": 1, "DBH": 1, "GH": 1, "MH": 1, "MC": 3},
        "MC" : {"DBH": 1, "LH": 3, "AD": 4, "SGMH": 4},
        "MH": {"CPAC": 2, "DBH": 1, "GC": 2, "GH": 2, "H": 3, "LH": 1},
        
            }

#Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

#Run the app
if __name__ == '__main__':
    app.run(debug=True)