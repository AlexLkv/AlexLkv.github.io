from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Function to parse the number from another site
def get_number():
    url = 'https://lk.abitur.mtuci.ru/list/spisok.php?levelTarget=bak_main&originalView=all&group=09.03.01+Искусственный+интеллект+и+машинное+обучение+%28Бюджет%2C+Очная%29+%282024%29&originalFilter=&topPriority=&search_type=snils&valueSearch=&originalView=rating'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    target_text = '193-037-041 53'  # Text to search
    elements = soup.find_all(string=lambda text: text and target_text in text)
    message = "Не удалось найти ваше место в рейтинге."

    if not elements:
        print(f"No elements found with text containing '{target_text}'")
        return message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for element in elements:
        print(f"Target text found: {element}")
        parent = element.parent
        if parent:
            previous_sibling = parent.find_previous_sibling()
            if previous_sibling:
                count = f"{previous_sibling.get_text(strip=True)}"
                message = f"Ваше актуальное место в рейтинге: {count}"
                print(message)
                return message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Home page
@app.route('/')
def home():
    number, last_update = get_number()
    return render_template('home.html', number=number, last_update=last_update)

if __name__ == '__main__':
    app.run(debug=True)
