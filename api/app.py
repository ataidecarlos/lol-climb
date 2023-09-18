from flask import Flask, render_template
from dataclasses import dataclass
import rito

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')

   summoner_id = rito.get_summoner_id('Thebausffs')
   if type(summoner_id) == int:
      print(f'Error: {summoner_id}')
      return render_template('error.html')
   else:
      thebausffs: rito.Summoner = rito.get_summoner_details(summoner_id)
      return render_template('index.html', league_points = thebausffs.league_points)

if __name__ == '__main__':
   app.run()