from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class UserFlowE2ETest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()  # ou Chrome selon ton setup

    def tearDown(self):
        self.browser.quit()

    def test_register_and_login_flow(self):
        # Inscription
        self.browser.get(f"{self.live_server_url}{reverse('register')}")
        self.browser.find_element(By.NAME, "username").send_keys("e2euser")
        self.browser.find_element(By.NAME, "email").send_keys("e2e@user.com")
        self.browser.find_element(By.NAME, "password1").send_keys("StrongPass123")
        self.browser.find_element(By.NAME, "password2").send_keys("StrongPass123")
        self.browser.find_element(By.CSS_SELECTOR, "form button").click()

        # Connexion
        self.browser.get(f"{self.live_server_url}{reverse('login_view')}")
        self.browser.find_element(By.NAME, "email").send_keys("e2e@user.com")
        self.browser.find_element(By.NAME, "password").send_keys("StrongPass123")
        self.browser.find_element(By.CSS_SELECTOR, "form button").click()

        # Vérifier qu’on est connecté
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Déconnexion", body_text)
