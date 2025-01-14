import streamlit as st
import json
import random


# Funcție pentru a încărca întrebările din fișier JSON
def incarca_intrebari(fisier_json, numar_intrebari):
    try:
        with open(fisier_json, 'r', encoding='utf-8') as f:
            toate_intrebari = json.load(f)
            if len(toate_intrebari) >= numar_intrebari:
                return random.sample(toate_intrebari, numar_intrebari)
            else:
                st.error("Fișierul nu conține suficiente întrebări.")
                return []
    except FileNotFoundError:
        st.error(f"Fișierul {fisier_json} nu a fost găsit.")
        return []
    except ValueError:
        st.error("Fișierul JSON nu are structura corectă.")
        return []


# Funcție pentru afișarea unei întrebări
def afiseaza_intrebare(intrebare):
    st.write(f"### {intrebare['intrebare']}")
    optiuni = intrebare['optiuni']
    alegere = st.radio("Alege răspunsul:", [op['text'] for op in optiuni], key=intrebare['intrebare'])
    return alegere


# Aplicația Streamlit
def main():
    st.title("Test de personalitate")

    # Inițializare sesiune
    if 'intrebari' not in st.session_state:
        st.session_state.intrebari = []

    if 'scoruri' not in st.session_state:
        st.session_state.scoruri = {"Pisică": 0, "Câine": 0, "Iepure": 0, "Pasăre": 0}

    if 'pagina' not in st.session_state:
        st.session_state.pagina = 0

    # Încarcă întrebările la început
    if not st.session_state.intrebari:
        st.session_state.intrebari = incarca_intrebari('intrebari.json', 15)

    def incrementare_pagina(intrebare_curenta, raspuns):
        for i, opt in enumerate(intrebare_curenta['optiuni']):
            if opt['text'] == raspuns:
                animal = opt['animal']
                st.session_state.scoruri[animal] += intrebare_curenta['scoruri'][i]
        st.session_state.pagina += 1

    # Dacă întrebările sunt încărcate, treci prin ele
    if st.session_state.pagina < len(st.session_state.intrebari):
        intrebare_curenta = st.session_state.intrebari[st.session_state.pagina]
        raspuns = afiseaza_intrebare(intrebare_curenta)
        st.button('Următoarea întrebare', on_click=incrementare_pagina, args=[intrebare_curenta, raspuns])



    # După ce toate întrebările sunt parcurse
    else:
        st.write("## Rezultate finale:")
        scoruri = st.session_state.scoruri
        scor_total = sum(scoruri.values())

        if scor_total > 0:
            procentaje = {animal: (scor / scor_total) * 100 for animal, scor in scoruri.items()}
            rezultat = max(procentaje, key=procentaje.get)



            st.success(f"Animalul care te reprezintă este: {rezultat}")

            st.write("### Detalii scoruri:")

            # Sortare procentaje în ordine descrescătoare
            procentaje_sortate = sorted(procentaje.items(), key=lambda x: x[1], reverse=True)

            for animal, procent in procentaje_sortate:
                st.write(f"{animal}: {procent:.2f}%")
        else:
            st.warning("Nu a fost selectat niciun răspuns.")

        def reincepe_quiz():
            st.session_state.pagina = 0
            st.session_state.intrebari = []
            st.session_state.scoruri = {"Pisică": 0, "Câine": 0, "Iepure": 0, "Pasăre": 0}

        st.button("Reîncepe quiz-ul", on_click=reincepe_quiz, args=[])


if __name__ == "__main__":
    main()