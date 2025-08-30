💻 Handelskalkulator

Ein interaktiver Handelskalkulator mit grafischer Benutzeroberfläche (GUI), entwickelt in Python und der Tkinter-Bibliothek. Das Tool ermöglicht eine schnelle und präzise Kalkulation der Handelsspanne, sowohl in Vorwärts- als auch in Rückwärtsrichtung.

Das Projekt ist Teil meines Portfolios und demonstriert die Fähigkeit, ein kommandozeilenbasiertes Skript in eine benutzerfreundliche Desktop-Anwendung zu verwandeln.

🌟 Funktionen

Zweistufige Kalkulation: Berechnet die Handelsspanne entweder von den Einkaufspreisen zu den Verkaufspreisen (Vorwärtskalkulation) oder umgekehrt (Rückwärtskalkulation). 
Intuitive GUI: Bietet eine saubere, moderne und einfach zu bedienende Benutzeroberfläche.
Fehlerbehandlung: Fängt ungültige Benutzereingaben ab und zeigt hilfreiche Fehlermeldungen an.
Anpassbares Design: Das Design ist thematisch an mein persönliches Wallpaper angelehnt, mit dunklen Farben und leuchtenden Akzenten.

💡 Wie es funktioniert

Der Rechner basiert auf den in der kaufmännischen Ausbildung gängigen Kalkulationsschemata. Er verarbeitet alle relevanten Posten wie Rabatte, Skonti, Bezugskosten und prozentuale Zuschläge. Die Berechnung erfolgt automatisch, sobald alle erforderlichen Werte eingegeben sind.

Der Code ist in zwei Hauptteile gegliedert:

1.  Kernlogik (Kalkulationsfunktionen): Zwei Python-Funktionen, `vorwaertskalkulation()` und `rueckwaertskalkulation()`, die die gesamte mathematische Logik enthalten.
2.  GUI-Logik (Tkinter-Klasse): Eine Klasse namens `HandelsrechnerApp`, die das grafische Fenster, die Widgets (Eingabefelder, Buttons, Radio-Buttons) und die Interaktion mit dem Benutzer verwaltet.

🚀 Nutzung

Voraussetzungen

Stelle sicher, dass Python auf deinem System installiert ist. Die benötigten Bibliotheken (Tkinter) sind standardmäßig in den meisten Python-Installationen enthalten.

Ausführen des Programms

1.  Klone dieses Repository oder lade die Datei `Handelskalkulator.py` herunter.
2.  Öffne dein Terminal oder die Eingabeaufforderung.
3.  Navigiere in das Verzeichnis, in dem sich die Datei befindet.
4.  Führe das Skript mit dem folgenden Befehl aus:

    ```bash
    python Handelskalkulator.py
    ```

🤝 Beitrag

Ich freue mich über Feedback und Anregungen zur Verbesserung des Projekts. Solltest du Fehler finden oder Vorschläge haben, öffne bitte ein Issue in diesem Repository.

📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
