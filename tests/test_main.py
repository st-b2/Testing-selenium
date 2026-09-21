import pytest
from faker import Faker
from pages.form_page import FormPage

fake = Faker()

def test_full_form(driver):
    data = {
        "name": fake.name(),
        "password": fake.password(length=10),
        "drinks": ["Water", "Coffee"],
        "color": "Yellow",
        "automation": "yes",
        "email": fake.email(),
        "message": "Привет!\nВторая строка.",
    }

    page = FormPage(driver).load()
    alert_text = page.fill(data).submit_n_read_alert()

    assert "Message received" in alert_text