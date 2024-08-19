from flask import Flask, request
import urllib
import ssl

context = ssl._create_unverified_context()
#Kontrollerar att index är online
def test_Is_online_index():
    assert urllib.request.urlopen("http://127.0.0.1:5000/", context=context, timeout=10)
#kontrollerar att form endpointen är online
def test_Is_online_form():
    assert urllib.request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10)
#kontrollerar att api är online
def test_is_online_external_api():
    assert urllib.request.urlopen("https://www.elprisetjustnu.se/api/v1/prices/2022/11-25_SE3.json", context=context, timeout=10)
