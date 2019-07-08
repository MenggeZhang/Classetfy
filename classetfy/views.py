import os
import sys
import random
import glob
import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import socket
import requests
from flask import Flask, jsonify, render_template, request
import time
from classetfy.scraper import Scraper
from classetfy import classetfy_rf
from classetfy import app

app.config["JSON_SORT_KEYS"] = False # keep order of jsonify objects

@app.route("/")
def index():
    return render_template('single_ip.html')

@app.route("/classetfy")
def classetfy():
    return render_template('single_ip.html')

@app.route("/single_ip_analysis", methods=["GET"])
def single_ip_analysis():
    result = {}
    ip_addr = request.args.get('ip_addr', '').strip()
    analysis1 = request.args.get('analysis1', '')
    analysis2 = request.args.get('analysis2', '')
    analysis3 = request.args.get('analysis3', '')
    if not ip_addr:
        result['status'] = 'failure'
        result['error_msg'] = 'Input is empty.'
        return jsonify(result) 
    try:
        scraper = Scraper(ip_addr)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        error_msg = str(e)
        result['status'] = 'failure'
        result['error_msg'] = error_msg
        return jsonify(result)

    result['status'] = 'success'

    TOP_FREQ_DISPLAY = 25
    if analysis1: result['analysis_1_result'] = scraper.tag_frequencies(TOP_FREQ_DISPLAY)
    if analysis2: result['analysis_2_result'] = scraper.tag_inner_text_words_frequencies()
    if analysis3: result['analysis_3_result'] = classetfy_rf.classify_with_rf(scraper.tag_frequencies())
    return jsonify(result)

def valid_ip(ip_addr):
    return True
    try:
        socket.inet_aton(ip_addr)
        return True
    except socket.error:
        return False

def ip_to_html_content(ip_addr):
    # given ip address, return the corresponding html content (string)
    
    res = requests.get('http://' + ip_addr, verify=False)
    res_text = res.text
        # return "<html>xxx</html>"
    return res_text
