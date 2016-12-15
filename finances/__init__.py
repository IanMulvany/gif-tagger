from flask import Flask, request, redirect, url_for, render_template, session, escape, jsonify
from redissession import RedisSessionInterface

app = Flask(__name__)
app.session_interface = RedisSessionInterface()
app.secret_key = b'thisisaveryveryverysecretkey'

import finances.views
