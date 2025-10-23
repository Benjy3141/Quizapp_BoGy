from flask import Flask, request, session, redirect, url_for
import time, random, json, os

app = Flask(__name__)
app.secret_key = "secret_key"

# Highscore-Datei
HIGHSCORE_FILE = "highscores.json"

# Initialisiere Highscores
if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump([], f)
#wie viele Fragen gestellt werden (max. 35 (wird automatisch auf 35 runtergesetzt) wegen nicht genug speicherplatz in session(liste))
QUESTION_COUNT = 10


# Fragen
pages = {
    1: {
        "title": "In welcher Einheit wird Elektrizität gemessen?",
        "buttons": ["Kilo Watt Stunden (kWh)", "Mol pro Gramm (mol/g)", "Pascal", "Meter (m)"],
        "correct": "Kilo Watt Stunden (kWh)"
    },
    2: {
        "title": "Wie wird Kommunikation reguliert?",
        "buttons": ["über Discord", "durch die BNetzA", "durch ANetzC", "durch den Präsidenten"],
        "correct": "durch die BNetzA"
    },
    3: {
        "title": "Wofür steht PV im Energiebereich?",
        "buttons": ["Power Volt", "Pressure Vacuum", "Photovoltaik", "Present Value"],
        "correct": "Photovoltaik"
    },
    4: {
        "title": "Was wird in Solarmodulen verwendet?",
        "buttons": ["Kupfer", "Aluminium", "Plastik", "Silizium"],
        "correct": "Silizium"
    },
    5: {
        "title": "Wer produziert die meiste Solarenergie?",
        "buttons": ["Deutschland", "Indien", "China", "USA"],
        "correct": "China"
    },
    6: {
        "title": "Was beschreibt die Marktlokation (MaLo) im Strommarkt am besten?",
        "buttons": ["Den physischen Zähler im Keller", "Den abrechnungsrelevanten Ort des Energieverbrauchs oder der Erzeugung", "Den Netzbetreiberbereich", "Den Lieferantenwechselprozess"],
        "correct": "Den abrechnungsrelevanten Ort des Energieverbrauchs oder der Erzeugung"
    },
    6: {
        "title": "Was beschreibt die Marktlokation (MaLo) im Strommarkt am besten?",
        "buttons": ["Den physischen Zähler im Keller", "Den abrechnungsrelevanten Ort des Energieverbrauchs oder der Erzeugung", "Den Netzbetreiberbereich", "Den Lieferantenwechselprozess"],
        "correct": "Den abrechnungsrelevanten Ort des Energieverbrauchs oder der Erzeugung"
    },
    7: {
        "title": "Wofür steht die Messlokation im Messwesen?",
        "buttons": ["Für den Liefervertrag", "Für den standardisierten Datenaustausch", "Für den konkreten Messzählpunkt (Zähler)", "Für die Anschlussleistung"],
        "correct": "Für den konkreten Messzählpunkt (Zähler)"
    },
    8: {
        "title": "Welche Rolle hat der Verteilnetzbetreiber (VNB) primär?",
        "buttons": ["Einkauf und Lieferung von Strom", "Betrieb und Stabilisierung des Verteilnetzes sowie Netzausbau vor Ort", "Betrieb des Übertragungsnetzes", "Direktvermarktung großer Erzeugungsanlagen"],
        "correct": "Betrieb und Stabilisierung des Verteilnetzes sowie Netzausbau vor Ort"
    },
    9: {
        "title": "Welche Aufgabe hat der Lieferant (LF)?",
        "buttons": ["Betrieb von Messeinrichtungen", "Verteilung der Stammdaten", "Einkauf und Lieferung von Strom", "Genehmigung von Bauvorhaben"],
        "correct": "Einkauf und Lieferung von Strom"
    },
    10: {
        "title": "Wofür ist der Messstellenbetreiber (MSB) verantwortlich?",
        "buttons": ["Stabilisierung des Übertragungsnetzes", "Betrieb der Messeinrichtungen und Datenerhebung", "Genehmigungen für Erzeugungsanlagen", "Ausbau der Überlandnetze"],
        "correct": "Betrieb der Messeinrichtungen und Datenerhebung"
    },
    11: {
        "title": "Welche Aufgabe hat der Übertragungsnetzbetreiber (ÜNB)?",
        "buttons": ["Kundenbelieferung und Abrechnung", "Betrieb und Stabilisierung des Übertragungsnetzes", "Montage von Zählern", "Zuweisung von Marktlokations-IDs"],
        "correct": "Betrieb und Stabilisierung des Übertragungsnetzes"
    },
    12: {
        "title": "Seit wann erfolgt die Marktkommunikation verpflichtend per AS4?",
        "buttons": ["01.01.2022", "01.10.2023", "01.04.2020", "31.12.2023"],
        "correct": "01.10.2023"
    },
    13: {
        "title": "Welcher Nachrichtentyp gehört zur EDIFACT-Marktkommunikation?",
        "buttons": ["JSONML", "UTILMD", "SOAPENV", "XMLX12"],
        "correct": "UTILMD"
    },
    14: {
        "title": "Welcher EDIFACT-Typ wird für Messwerte häufig genutzt?",
        "buttons": ["IFTSTA", "CONTRL", "MSCONS", "APERAK"],
        "correct": "MSCONS"
    },
    15: {
        "title": "Was kennzeichnet SLP im EDM-Kontext?",
        "buttons": ["Viertelstundenwerte registriert", "Standardlastprofile ohne registrierenden Lastgang", "Halbstundenleistungen für Industriekunden", "Prognosefreie Zeitreihen"],
        "correct": "Standardlastprofile ohne registrierenden Lastgang"
    },
    16: {
        "title": "Wofür steht RLM?",
        "buttons": ["Regel-Leistungs-Management", "Registrierende Lastgangmessung", "Regional Lastgemittelter Messwert", "Rücklieferungsmanagement"],
        "correct": "Registrierende Lastgangmessung"
    },
    17: {
        "title": "Was beschreibt eine OBIS-Kennzahl wie 1-1:1.8.0?",
        "buttons": ["Eine Netztopologie-ID", "Einen Zählpunktbetreiber", "Eine standardisierte Messwertart/Channel", "Eine Lieferantenbilanz-kreisschlüsselnummer"],
        "correct": "Eine standardisierte Messwertart/Channel"
    },
    18: {
        "title": "Welche Wertearten gibt es laut EDM 1x1?",
        "buttons": ["Echte, Roh-, und Delta-Werte", "Vorläufige, Ersatz- und wahre Werte", "Prognose-, Schätz- und Zählwerte", "Roh-, Validierte- und Forecast-Werte"],
        "correct": "Vorläufige, Ersatz- und wahre Werte"
    },
    19: {
        "title": "Welcher Zählertyp ist der klassische elektromechanische Drehscheibenzähler?",
        "buttons": ["MME", "Smart Meter Gateway", "Ferraris-Zähler", "PLC-Zähler"],
        "correct": "Ferraris-Zähler"
    },
    20: {
        "title": "Was ist eine Moderne Messeinrichtung (MME)?",
        "buttons": ["Das Kommunikationsmodul des ÜNB", "Ein digitaler Zähler ohne Gateway-Fernauslesung", "Ein Lastmanagementsystem", "Ein Erzeugungszähler für PV"],
        "correct": "Ein digitaler Zähler ohne Gateway-Fernauslesung"
    },
    21: {
        "title": "Wofür steht ein Smart Meter Gateway im Messsystem?",
        "buttons": ["Für die physische Energieumwandlung", "Für die Verschlüsselung von E-Mails", "Für die sichere Kommunikation und Steuerbarkeit des Messsystems", "Für die Netzwiederherstellung nach Ausfällen"],
        "correct": "Für die sichere Kommunikation und Steuerbarkeit des Messsystems"
    },
    22: {
        "title": "Welcher Herstellerpräfix passt korrekt zum Zählerhersteller Landis+Gyr?",
        "buttons": ["1LGZ", "1ELS", "1ITR", "1ISK"],
        "correct": "1LGZ"
    },
    23: {
        "title": "Was ist ein Vorteil eines wettbewerblichen MSB (wMSB)?",
        "buttons": ["Gesetzliche Monopolstellung im Netzgebiet", "Bessere Planbarkeit/Controlling für überregional tätige Unternehmen", "Zugang zu Übertragungsnetzregelenergie", "Verpflichtung zur Direktvermarktung"],
        "correct": "Bessere Planbarkeit/Controlling für überregional tätige Unternehmen"
    },
    24: {
        "title": "In welchem Kontext kann sich ein wMSB besonders spezialisieren?",
        "buttons": ["Straßenbeleuchtungsverträge", "Blockchain-Modelle, Erzeugungsanlagen, Kundenanlagen", "Nur Gaszählung", "Nur Stromlieferung"],
        "correct": "Blockchain-Modelle, Erzeugungsanlagen, Kundenanlagen"
    },
    25: {
        "title": "Was zeigt das Beispiel „Mieterstrom“ typischerweise?",
        "buttons": ["Nur einen einzelnen Haushaltszähler", "Eine einfache Einfamilienhausstruktur", "Ein komplexes Konstrukt mit PV und mehreren Wohnungszählern", "Ein Industriekundenprofil ohne PV"],
        "correct": "Ein komplexes Konstrukt mit PV und mehreren Wohnungszählern"
    },
    26: {
        "title": "Welche Marktrolle verantwortet die Direktvermarktung großer Erzeugungsanlagen?",
        "buttons": ["VNB", "ÜNB", "Lieferant", "MSB"],
        "correct": "Lieferant"
    },
    27: {
        "title": "Wer genehmigt Bauvorhaben von Verbrauchern und Erzeugern an das Netz?",
        "buttons": ["Lieferant", "VNB", "MSB", "ÜNB"],
        "correct": "VNB"
    },
    28: {
        "title": "Welches BNetzA-Werk regelt die Kundenbelieferungsprozesse mit Elektrizität?",
        "buttons": ["WiM", "GPKE", "MaBiS", "StromNEV"],
        "correct": "GPKE"
    },
    29: {
        "title": "Welches BNetzA-Werk regelt Wechsel im Messwesen?",
        "buttons": ["MaKo 2020", "GPKE", "WiM", "GeLi Gas"],
        "correct": "WiM"
    },
    30: {
        "title": "Welche Technologie ersetzt in der Marktkommunikation die verschlüsselte E-Mail?",
        "buttons": ["S/MIME", "AS4", "AS2", "XMPP"],
        "correct": "AS4"
    },
    31: {
        "title": "Welcher EDIFACT-Typ dient primär der Stammdatenkommunikation?",
        "buttons": ["UTILMD", "APERAK", "MSCONS", "IFTSTA"],
        "correct": "UTILMD"
    },
    32: {
        "title": "Wofür wird APERAK in der Marktkommunikation genutzt?",
        "buttons": ["Für Messwertlieferungen", "Für technische Syntaxbestätigungen", "Für applikationsbezogene Bestätigungen/Rückmeldungen", "Für Bilanzkreisabrechnung"],
        "correct": "Für applikationsbezogene Bestätigungen/Rückmeldungen"
    },
    33: {
        "title": "Was beschreibt IFTSTA typischerweise?",
        "buttons": ["Statusmeldungen zu Prozessfortschritten", "Lieferantenermächtigungen", "OBIS-Definitionen", "Netzausbaupläne"],
        "correct": "Statusmeldungen zu Prozessfortschritten"
    },
    34: {
        "title": "Welche Aussage trifft zu „wahren Werten“ im EDM?",
        "buttons": ["Sie ersetzen fehlerhafte Messungen", "Es sind geprüfte/valide Originalmesswerte", "Es sind reine Prognosewerte", "Es sind hochgerechnete Ersatzwerte"],
        "correct": "Es sind geprüfte/valide Originalmesswerte"
    },
    35: {
        "title": "Was beschreibt „Ersatzwerte“ im EDM?",
        "buttons": ["Werte nach Schätzung bei Ausfall/Fehlern", "Vorläufige Rohdaten vom Zähler", "Endgültige, geeichte Werte", "Prognosen des Lieferanten"],
        "correct": "Werte nach Schätzung bei Ausfall/Fehlern"
    },
    36: {
        "title": "Welche Zeitreihenauflösung ist typisch für RLM-Messung?",
        "buttons": ["60 Minuten", "30 Minuten", "15 Minuten", "5 Minuten"],
        "correct": "15 Minuten"
    },
    37: {
        "title": "Welche Aussage passt zur OBIS-Kennzahlensystematik?",
        "buttons": ["Sie ist herstellerindividuell", "Sie ist eine BNetzA-standardisierte Codierung", "Sie wird nur im Gasbereich genutzt", "Sie ersetzt EDIFACT"],
        "correct": "Sie ist eine BNetzA-standardisierte Codierung"
    },
    38: {
        "title": "Was unterscheidet MME vom intelligenten Messsystem?",
        "buttons": ["MME misst nicht digital", "Intelligentes Messsystem = MME + Gateway", "MME hat immer Fernauslesung", "Intelligentes Messsystem hat keinen Zähler"],
        "correct": "Intelligentes Messsystem = MME + Gateway"
    },
    39: {
        "title": "Welcher Herstellerpräfix ist korrekt zugeordnet?",
        "buttons": ["Itron – 1ITR", "Elster – 1ISK", "Easymeter – 1ITR", "Iskra – 1ESY"],
        "correct": "Itron – 1ITR"
    },
    40: {
        "title": "Welches Ziel verfolgen wMSB für Letztverbraucher besonders?",
        "buttons": ["Abschaffung von Grundgebühren", "Angebot zusätzlicher Mehrwerte/Services", "Reduktion der EEG-Umlage", "Befreiung von Netzentgelten"],
        "correct": "Angebot zusätzlicher Mehrwerte/Services"
    },
    41: {
        "title": "Wozu dient die Spezialisierung eines wMSB auf Kundenanlagen?",
        "buttons": ["Zur Senkung der Netzverluste", "Zur effizienten Abwicklung komplexer Mess- und Abrechnungsstrukturen", "Zur Erzeugung von Regelenergie", "Zur Festlegung von Netzentgelten"],
        "correct": "Zur effizienten Abwicklung komplexer Mess- und Abrechnungsstrukturen"
    },
    42: {
        "title": "Was zeigt das Mieterstrom-Beispiel im Hinblick auf Zählstrukturen?",
        "buttons": ["Eine reine Erzeugungsanlage ohne Verbraucher", "Einfache Einzählerlösung", "Mehrere Wohnungszähler plus PV-Einspeisezähler", "Nur Gewerbezähler"],
        "correct": "Mehrere Wohnungszähler plus PV-Einspeisezähler"
    },
    43: {
        "title": "Welcher Partner verteilt Stammdaten innerhalb der Marktprozesse?",
        "buttons": ["ÜNB", "VNB", "MSB", "Lieferant"],
        "correct": "VNB"
    },
    44: {
        "title": "Welche Nachricht dient der technischen Syntaxbestätigung im EDIFACT-Austausch?",
        "buttons": ["IFTSTA", "CONTRL", "APERAK", "MSCONS"],
        "correct": "CONTRL"
    },
    45: {
        "title": "Welche typische ID-Repräsentation findet man an elektronischen Zählern zur Herstellerkennung?",
        "buttons": ["Freitext ohne Schema", "OBIS-Prefix", "Herstellerpräfix wie 1LGZ, 1ITR, 1ESY", "Bilanzkreis-ID"],
        "correct": "Herstellerpräfix wie 1LGZ, 1ITR, 1ESY"
    },
}

if QUESTION_COUNT >len(pages):
    QUESTION_COUNT=len(pages)

if QUESTION_COUNT >35:
    QUESTION_COUNT=35

def load_highscores():
    with open(HIGHSCORE_FILE, "r") as f:
        return json.load(f)


def save_highscore(name, score):
    scores = load_highscores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]  # nur Top 10 speichern
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f)


@app.route("/", methods=["GET", "POST"])
def start_page():
    if request.method == "POST":
        session.clear()
        session["question_order"] = random.sample(list(pages.keys()), QUESTION_COUNT)  # zufällige Reihenfolge   falls man alle fragen fragen möchte:"len(pages)"" anstatt 10
        session["page_index"] = 0
        session["answers"] = {}
        session["score"] = 0
        session["used_5050"] = {}
        session["started"] = True
        session["shuffled_buttons"] = {}
        session["joker_used"] = False
        session["joker_removed_options"] = {}
        return redirect(url_for("quiz"))

    return """
    <div style="text-align: center; margin-top: 100px;">
        <h1 style="font-size: 40px;">🎮 Willkommen zum Quiz</h1>
        <p style="font-size: 20px;">Klicke auf „Spiel starten“, um zu beginnen. Versuche dann, die Fragen so schnell wie möglich richtig zu beantworten,
        <p style="font-size: 20px;">um möglichst viele Punkte zu gewinnen. Je schneller du antwortest, desto mehr Punkte erhältst du. 
        <p style="font-size: 20px;">Du hast einen 50-50 Joker, durch den es bei einer Frage nur noch 2 Antwortsmöglichkeiten gibt.
        <form method="post">
            <button type="submit" style="padding: 16px 32px; font-size: 24px;">▶️ Spiel starten</button>
        </form>
    </div>
    """

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not session.get("started"):
        return redirect(url_for("start_page"))

    question_order = session["question_order"]
    index = session.get("page_index", 0)

    if index >= len(question_order):
        return redirect(url_for("end_page"))

    current_id = question_order[index]
    current_page = pages[current_id]
    correct_button = current_page["correct"]

    if "shuffled_buttons" not in session:
        session["shuffled_buttons"] = {}

    if str(current_id) not in session["shuffled_buttons"]:
        shuffled = current_page["buttons"][:]
        random.shuffle(shuffled)
        session["shuffled_buttons"][str(current_id)] = shuffled
    else:
        shuffled = session["shuffled_buttons"][str(current_id)]

    if "start_time" not in session:
        session["start_time"] = time.time()

    if "joker_used" not in session:
        session["joker_used"] = False

    if "joker_removed_options" not in session:
        session["joker_removed_options"] = {}

    answered = str(current_id) in session["answers"]
    selected_button = None
    answer_data = {}

    if answered:
        answer_data = session["answers"][str(current_id)]
        selected_button = answer_data["selected"]

    # Verarbeitung der POST-Aktionen
    if request.method == "POST":
        clicked = request.form.get("button")

        if clicked == "next":
            session["page_index"] = index + 1
            session.pop("start_time", None)
            return redirect(url_for("quiz"))

        elif clicked == "5050" and not session["joker_used"] and not answered:
            buttons = session["shuffled_buttons"][str(current_id)]
            incorrect = [b for b in buttons if b != correct_button]
            to_remove = random.sample(incorrect, 2)
            session["joker_removed_options"][str(current_id)] = to_remove
            session["joker_used"] = True
            return redirect(url_for("quiz"))

        elif clicked and not answered:
            end_time = time.time()
            time_taken = end_time - session["start_time"]
            points = max(1, int(1000 * (1 / (1 + time_taken / 10))))

            if clicked != correct_button:
                points = 0

            session["score"] += points
            session["answers"][str(current_id)] = {
                "selected": clicked,
                "points": points,
                "correct": correct_button,
                "time": round(time_taken, 2)
            }

            return redirect(url_for("quiz"))

    # Fortschrittsbalken
    progress = int((index + 1) / QUESTION_COUNT * 100)
    progress_bar = f"""
    <div style="width: 80%; margin: 20px auto; height: 25px; background-color: #ddd; border-radius: 10px; overflow: hidden;">
        <div style="height: 100%; width: {progress}%; background-color: #4CAF50;"></div>
    </div>
    """

    # Entfernte Optionen durch 50:50 Joker
    removed_options = session["joker_removed_options"].get(str(current_id), [])

    # Antwort-Buttons
    buttons_html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; justify-items: center; max-width: 800px; margin: 0 auto;">'
    for b in shuffled:
        if b in removed_options:
            continue  # Button wird durch 50:50 entfernt

        style = "width: 320px; height: 110px; font-size: 22px; cursor: pointer;"
        disabled = ""

        if answered:
            disabled = "disabled"
            if b == correct_button:
                style += " background-color: lightgreen;"
            elif b == selected_button:
                style += " background-color: lightcoral;"
            else:
                style += " opacity: 0.5;"

        buttons_html += f'''
            <button type="submit" name="button" value="{b}" {disabled}
                style="{style}">
                {b}
            </button>
        '''
    buttons_html += "</div>"

    # 50:50 Joker Button
    joker_disabled = "disabled" if session["joker_used"] or answered else ""
    joker_style = "padding: 10px 20px; font-size: 20px; margin: 30px; cursor: pointer;"
    joker_style += " background-color: gray;" if session["joker_used"] else " background-color: #007BFF; color: white;"

    joker_button_html = f"""
    <form method="post">
        <button type="submit" name="button" value="5050" {joker_disabled}
            style="{joker_style}">
            50:50 Joker
        </button>
    </form>
    """

    # Nächste Frage Button
    next_button_html = ""
    if answered:
        next_button_html = f"""
        <div style="margin-top: 40px; font-size: 24px;">
            <p style="font-size: 28px;">Du hast <strong>{answer_data['points']}</strong> Punkte erhalten</p>
            <p style="font-size: 28px;">Gesamtpunktzahl: <strong>{session['score']}</strong></p>
        </div>
        <form method="post" style="margin-top: 30px;">
            <button type="submit" name="button" value="next"
                style="padding: 20px 40px; font-size: 28px; cursor: pointer;">➡️ Weiter</button>
        </form>
        """

    # Neustart oben rechts
    restart_button_html = f"""
    <div style="position: absolute; top: 10px; right: 20px;">
        <form action="/" method="get">
            <button type="submit"
                style="padding: 10px 20px; font-size: 20px; background-color: #eee; border: 1px solid #ccc; cursor: pointer;">
                🔄 Neustart
            </button>
        </form>
    </div>
    """

    return f"""
    <div style="text-align: center; margin-top: 80px; position: relative;">
        {restart_button_html}
        {progress_bar}
        <h1 style="font-size: 36px; margin-bottom: 40px;">{current_page['title']}</h1>
        {joker_button_html}
        <form method="post">
            {buttons_html}
        </form>
        {next_button_html}
    </div>
    """

@app.route("/end", methods=["GET", "POST"])
def end_page():
    if not session.get("started"):
        return redirect(url_for("start_page"))

    total_score = session.get("score", 0)
    correct_count = len([a for a in session["answers"].values() if a["selected"] == a["correct"]])
    total_questions = len(session.get("question_order", []))

    if request.method == "POST":
        name = request.form.get("name", "Spieler").strip()

        # Begrenze den Namen auf 20 Zeichen
        if len(name) > 20:
            return """
            <div style="text-align: center; margin-top: 100px;">
                <h1 style="font-size: 32px; color: red;">❌ Fehler</h1>
                <p style="font-size: 24px;">Der Name darf maximal 20 Zeichen lang sein.</p>
                <a href="/end" style="font-size: 20px; display: inline-block; margin-top: 20px;">🔙 Zurück</a>
            </div>
            """

        if name:
            save_highscore(name, total_score)
        session.clear()
        return redirect(url_for("highscore_page"))

    # 🔁 Restart-Button HTML
    restart_button_html = """
    <div style="position: absolute; top: 10px; right: 20px;">
        <form action="/" method="get">
            <button type="submit"
                style="padding: 10px 20px; font-size: 20px; background-color: #eee; border: 1px solid #ccc; cursor: pointer;">
                🔄 Neustart
            </button>
        </form>
    </div>
    """

    return f"""
    <div style="text-align: center; margin-top: 100px; position: relative;">
        {restart_button_html}
        <h1 style="font-size: 40px;">🎉 Spiel beendet!</h1>
        <p style="font-size: 24px;">Du hast <strong>{correct_count}</strong> von <strong>{total_questions}</strong> Fragen richtig beantwortet.</p>
        <p style="font-size: 28px; margin-top: 20px;"><strong>Gesamtpunktzahl:</strong> {total_score} Punkte</p>
        <form method="post" style="margin-top: 40px;">
            <input type="text" name="name" maxlength="20" placeholder="Dein Name (max. 20 Zeichen)" style="font-size: 20px; padding: 10px;" required />
            <button type="submit" style="padding: 12px 24px; font-size: 20px; margin-left: 10px;">📥 Highscore speichern</button>
        </form>
    </div>
    """


@app.route("/highscores")
def highscore_page():
    scores = load_highscores()

    score_rows = ""
    for idx, entry in enumerate(scores, start=1):
        score_rows += f"<tr><td>{idx}</td><td>{entry['name']}</td><td>{entry['score']}</td></tr>"

    return f"""
    <div style="text-align: center; margin-top: 60px;">
        <h1 style="font-size: 36px;">🏆 Highscores</h1>
        <table style="margin: 30px auto; font-size: 22px; border-collapse: collapse;">
            <tr style="background-color: #ddd;">
                <th style="padding: 10px 20px;">#</th>
                <th style="padding: 10px 20px;">Name</th>
                <th style="padding: 10px 20px;">Punkte</th>
            </tr>
            {score_rows if score_rows else '<tr><td colspan="3">Noch keine Einträge</td></tr>'}
        </table>
        <form action="/" method="get" style="margin-top: 30px;">
            <button type="submit" style="padding: 12px 28px; font-size: 20px;">🔁 Neues Spiel</button>
        </form>
        <form method="post" action="/reset" style="margin-top: 20px;">
            <button type="submit" style="padding: 10px 20px; font-size: 18px; background-color: #f55; color: white;">❌ Highscoretabelle leeren</button>
        </form>
    </div>
    """


@app.route("/reset", methods=["POST"])
def reset_highscores():
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump([], f)
    return redirect(url_for("highscore_page"))
