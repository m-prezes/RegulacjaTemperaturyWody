from flask import Flask, render_template, request
from plots import all_plots
from model import obiekt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(wartosc_zadana=35.0, Q2_max=30.0, T1=10.0, Q1=15.0, T2=70.0, V=10875.0, czas_symulacji=60*6, czas_anomalii=0, T_anomalii=0):
    if request.method == 'POST':
        wartosc_zadana = float(request.form['T_zadana'])
        Q2_max = float(request.form['Q2_max'])
        T1 = float(request.form['T1'])
        T2 = float(request.form['T2'])
        Q1 = float(request.form['Q1'])
        V = float(request.form['V'])
        czas_symulacji = float(request.form['czas_symulacji'])
        czas_anomalii = float(request.form['czas_anomalii'])
        T_anomalii = float(request.form['T_anomalii'])


    dane_do_wykresow, N, wskaznik_przeregulowania, const_p = obiekt(wartosc_zadana, Q2_max, T1, Q1, T2, V, czas_symulacji,czas_anomalii,T_anomalii)
    wskaznik_przeregulowania = round(wskaznik_przeregulowania, 4)
    wykresy = all_plots(N, dane_do_wykresow, const_p)

    d = wykresy[0]
    plot = d[0]
    plot2 = d[1]

    d = wykresy[1]
    plot3 = d[0]
    plot4 = d[1]

    d = wykresy[2]
    plot5 = d[0]
    plot6 = d[1]

    return render_template("index.html",
                           plot=plot,
                           plot2=plot2,
                           plot3=plot3,
                           plot4=plot4,
                           plot5=plot5,
                           plot6=plot6,
                           wskaznik=wskaznik_przeregulowania,
                           wartosc_zadana=wartosc_zadana,
                           Q2_max=Q2_max,
                           T1=T1,
                           T2=T2,
                           Q1=Q1,
                           V=V,
                           czas_symulacji=czas_symulacji,
                           czas_anomalii=czas_anomalii,
                           T_anomalii=T_anomalii,)


if __name__ == '__main__':
    app.run(debug=True)
