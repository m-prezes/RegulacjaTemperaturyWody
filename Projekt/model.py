import math


def obiekt(wartosc_zadana, q2_max, t1, q1, t2, v, czas_symulacji, czas_anomalii, t_anomalii):
    # Wartości dla I dopływu
    Q1 = q1
    T1 = t1
    # Wartości dla II dopływu - KONTROLOWANY
    T2 = t2
    Q2_max = q2_max
    Q2 = 0.5 * Q2_max

    # Objętość basenu
    V = v

    # Czas próbkowania
    const_p = 0.5
    N = int(1 / const_p * 60 * czas_symulacji)

    # Wartości początkowe w tablicach
    T_0 = cieplo(Q1,T1,Q2,T2)
    T_wartosci = [T_0]
    e = []
    pid = []
    u = []
    Q2_tab = [Q2]
    Q = []
    T_zadane_tab = [T_0]
    dostarczone_cieplo = []

    # Wartość zadana
    T_zadana = wartosc_zadana

    # Anomalia
    czas_anomalii = int(czas_anomalii * 60 * 1 / const_p)
    T_anomalii = t_anomalii
    tau = T1 * Q1 / V
    e_sum = 0

    for n in range(N):
        # Anomalia
        if czas_anomalii != 0 and n == czas_anomalii:
            T_wartosci[-1] = T_anomalii

        # Uchyb od wartości zadanej
        e_value = T_zadana - T_wartosci[n]
        e.append(e_value)
        e_sum +=e_value

        # Regulacja PID
        pid_value = regulacja_PID(e, e_sum, const_p, n)
        pid.append(pid_value)
        u.append(ograniczenie_PID(pid_value))

        # Wartość dopływu ciepłej wody
        Q2_tab.append(Q2_max * (0.5 + u[-1]/2))

        # Wartość odpływu
        Q.append(Q2_tab[-1] + Q1)

        # Wartość temperatury
        dostarczone_cieplo.append(cieplo(Q1, T1, Q2_tab[-1], T2))
        T_wartosci.append(temperatura(T_wartosci[-1], tau, const_p, T2, Q2_tab[-1], V, Q[-1]))
        T_zadane_tab.append(T_zadana)

    # Współczynnik przeregulowania
    k = wskaznik_przeregulowania(T_wartosci, T_zadana, T_0)

    return [["T(t)", T_wartosci, "T_zadana", T_zadane_tab], ["T_wejście", dostarczone_cieplo, "T_zbiornik", T_wartosci],
            ["u", u, "pid", pid]], N, k, const_p


def regulacja_PID(e, e_sum, const_p, n):
    # Wartości nastaw regulatora
    kp = 0.01
    Ti = 60
    Td = 2
    return kp * (e[n] + const_p / Ti * e_sum + Td / const_p * (e[n] - e[n - 1]))


def ograniczenie_PID(pid):
    if pid > 1:
        pid = 1
    if pid < -1:
        pid = -1
    return pid


def cieplo(Q1, T1, Q2, T2):
    return (Q1 * T1 + Q2 * T2) / (Q1 + Q2)


def temperatura(T, tau, const_p, T2, Q2, V, Q):
    return (tau + (T2 * Q2 - T * Q) / V) * const_p + T


# def wskaznik_przeregulowania(T, T_zadana):
#     return round(((max(T) - T_zadana) / T_zadana)*100,2)

def wskaznik_przeregulowania(T, T_zadana, t_0):
    if t_0 <= T_zadana:
        return abs(round(((max(T) - T_zadana) / T_zadana)*100,2))
    elif t_0 > T_zadana:
        return abs(round(((min(T) - T_zadana) / T_zadana) * 100, 2))