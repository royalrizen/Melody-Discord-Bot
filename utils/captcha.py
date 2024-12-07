import os
import urllib
import random
import pydub
import speech_recognition
import time
from playwright.async_api import async_playwright

class RecaptchaSolver:
    def __init__(self, page):
        self.page = page
    
    async def solveCaptcha(self):
        iframe_inner = await self.page.wait_for_selector('iframe[title="reCAPTCHA"]', timeout=10000)
        await iframe_inner.click()

        iframe = await self.page.query_selector("iframe[title='reCAPTCHA']")

        audio_button = await iframe.query_selector('#recaptcha-audio-button')
        if audio_button:
            await audio_button.click()
        
        await self.page.wait_for_timeout(300)
        
        audio_source = await iframe.query_selector('#audio-source')
        src = await audio_source.get_attribute('src')
        
        path_to_mp3 = os.path.join("/tmp", f"{random.randrange(1, 1000)}.mp3")
        path_to_wav = os.path.join("/tmp", f"{random.randrange(1, 1000)}.wav")
        urllib.request.urlretrieve(src, path_to_mp3)

        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = speech_recognition.AudioFile(path_to_wav)
        
        r = speech_recognition.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        
        key = r.recognize_google(audio)
        
        audio_response = await iframe.query_selector('#audio-response')
        await audio_response.fill(key.lower())

        await audio_response.press('Enter')

        await self.page.wait_for_timeout(400)

        if await self.isSolved():
            return True
        else:
            raise Exception("Failed to solve the CAPTCHA")

    async def isSolved(self):
        try:
            checkmark = await self.page.query_selector('.recaptcha-checkbox-checkmark')
            if checkmark:
                return True
            return False
        except Exception:
            return False

async def solve_captcha(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        recaptcha_solver = RecaptchaSolver(page)

        try:
            await recaptcha_solver.solveCaptcha()
            print("CAPTCHA solved successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
