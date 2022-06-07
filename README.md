# Stock Trading Bot for CSC-481
#### Instructor: Rodrigo Canaan at Cal Poly
#### Team Members:  Tushar Sharma, Gaurav Joshi, Beck Dehlsen, Maxim Korolkov
## About
This is a stock trading application in Python that allows users to build a portfolio of stocks from real-time market data using the Python Yahoo Finance API (yfinance) and then seek recommendations on whether to buy, sell, or hold each stock. The bot uses a command line interface to process information about the user\'s simulated stock portfolio and present feedback for any stock using a built-in inference engine.

Further information and details of evaluation can be found [here](https://docs.google.com/document/d/19uEnmPSunm7kgvbDkcNrbdXhvy7Vfv5o/edit?usp=sharing&ouid=117301202978037301813&rtpof=true&sd=true "here"). Evaluation was performed using QuantConnect via backtesting on historical data for individual stocks.
## Instructions
1. Install the latest version of Python
2. Clone the repository to a local directory of choice
3. Open a Bash terminal and install packages using the following commands:
```bash
pip install pandas --upgrade --no-cache-dir
pip install yfinance --upgrade --no-cache-dir
```
4. Run the application in the project's directory with 
```bash
python3 main.py
```
