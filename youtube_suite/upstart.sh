#!/usr/bin/env bash

apt-get -y update
apt-get -y install python3-pip

#dash
pip3 install dash==0.21.0  # The core dash backend
pip3 install dash-renderer==0.12.1  # The dash front-end
pip3 install dash-html-components==0.10.0  # HTML components
pip3 install dash-core-components==0.22.1  # Supercharged components
pip3 install plotly --upgrade  # Plotly graphing library used in examples

#beautiful soup
pip3 install beautifulsoup4

#pandas
pip3 install numpy
pip3 install pandas

#selenium setup
pip3 install selenium
