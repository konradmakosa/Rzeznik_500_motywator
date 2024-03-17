import requests
from bs4 import BeautifulSoup
from datetime import date

# Definicja funkcji znajdującej wiersz zawierający określony tekst
def find_row_with_text(soup, target_text):
    rows = soup.find_all('strong', class_='texdt-primary')  # Znajdź wszystkie wiersze zawierające określony tekst
    for row in rows:
        if row.text.strip() == target_text:  # Sprawdź, czy tekst w wierszu jest taki sam jak szukany tekst
            return row.parent.parent  # Jeśli tak, zwróć wiersz
    return None  # Jeśli nie znaleziono wiersza, zwróć None

# Dane logowania
username = 'konrad@makosa.org'
password = '5147raRA!'

# Adres URL strony, która wymaga uwierzytelnienia
url = 'https://wyniki.b4sport.pl/rzeznik-500/e5184.html'

# Przekazanie danych uwierzytelniających w zapytaniu HTTP
response = requests.get(url, auth=(username, password))

# Sprawdzenie, czy uzyskano dostęp do strony
if response.status_code == 200:
    html_content = response.content

    # Utworzenie obiektu BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tekst, którego szukamy w wierszu
    target_text = "MĄKOSA Konrad"

    # Znajdź wiersz na podstawie tekstu
    target_row = find_row_with_text(soup, target_text)

    if target_row:
        # Pobierz wszystkie komórki wiersza
        cells = target_row.find_all('td')

        # Sprawdź, czy wiersz ma wystarczającą liczbę komórek
        if len(cells) > 11:  # Sprawdzamy czy jest co najmniej 12 komórek, ponieważ indeksy liczymy od zera
            # Wyodrębnij tekst z odpowiedniej komórki (indeks 11) - kolejna komórka po nazwisku zawodnika
            numerical_value = cells[11].text.strip()

            numerical2_value = cells[11].text.strip()

            # Pobierz wszystkie wiersze
            rows = soup.find_all('strong', class_='texdt-primary')

            # Znajdź indeks wiersza zawierającego "MĄKOSA Konrad"
            target_row_index = [row.text.strip() for row in rows].index(target_text)

            # Znajdź wiersz o jedną pozycję wcześniej niż wiersz zawierający "MĄKOSA Konrad"
            previous_row_index = target_row_index - 1
            previous2_row_index = target_row_index - 2

            if previous_row_index >= 0:
                previous_row = rows[previous_row_index]
                previous2_row = rows[previous2_row_index]

                # Pobierz wszystkie komórki wiersza
                previous_cells = previous_row.parent.parent.find_all('td')
                previous2_cells = previous2_row.parent.parent.find_all('td')

                # Sprawdź, czy wiersz ma wystarczającą liczbę komórek
                if len(previous_cells) > 11:  # Sprawdzamy czy jest co najmniej 12 komórek, ponieważ indeksy liczymy od zera
                    # Wyodrębnij tekst z odpowiedniej komórki (indeks 11) - kolejna komórka po nazwisku zawodnika
                    previous_numerical_value = previous_cells[11].text.strip()

                    # Konwertuj obie wartości liczbowe na odpowiednią liczbę
                    previous_numerical_value = float(previous_numerical_value.replace(',', '.'))  # Zmiana przecinka na kropkę i konwersja na float
                    numerical_value = float(numerical_value.replace(',', '.'))  # Zmiana przecinka na kropkę i konwersja na float

                    # Oblicz różnicę między wartościami liczbowymi
                    difference = round(previous_numerical_value - numerical_value,2)

                # Sprawdź, czy wiersz ma wystarczającą liczbę komórek
                if len(previous2_cells) > 11:  # Sprawdzamy czy jest co najmniej 12 komórek, ponieważ indeksy liczymy od zera
                    # Wyodrębnij tekst z odpowiedniej komórki (indeks 11) - kolejna komórka po nazwisku zawodnika
                    previous2_numerical_value = previous2_cells[11].text.strip()

                    # Konwertuj obie wartości liczbowe na odpowiednią liczbę
                    previous2_numerical_value = float(previous2_numerical_value.replace(',', '.'))  # Zmiana przecinka na kropkę i konwersja na float
                    numerical2_value = float(numerical2_value.replace(',', '.'))  # Zmiana przecinka na kropkę i konwersja na float

                    # Oblicz różnicę między wartościami liczbowymi
                    difference2 = round(previous2_numerical_value - numerical2_value, 2)

    else:
        print("Nie znaleziono wiersza zawierającego tekst:", target_text)
else:
    print("Błąd podczas pobierania strony:", response.status_code)

# Obecna data
current_date = date.today()

# Data docelowa
target_date = date(2024, 5, 29)

# Obliczenie różnicy w dniach
days_until_target = (target_date - current_date).days

adjusted_value = round((500 - numerical_value) / days_until_target, 2)

# Wyświetlenie wyniku
print(f"Twoja pozycja:            {target_row_index+1}")
print(f"Przebiegłeś w sumie:      {numerical_value} km")
print(f"\nDo tego przed Tobą masz:  {difference} km")
print(f"A ten przed nim jest:     {difference2} km")
print(f"\nPowinieneś dziś \nprzebiec conajmniej:      {adjusted_value} km")