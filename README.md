# CSE111_Project
This repository is dedicated to backing-up and facilitating teamwork on the CSE111 final project.

To initialize tables use this command in bash: sqlite3 GameDB.sqlite < create-schema-GameDB.sql 
OR
Use generation files (i.e player.py) to create tables by running them: python3 player.py

To populate / drop entire database use python3 Master.py with / without commented sections
    This also functions to create tables

To run query file in terminal: 
1. bash
2. sqlite3 GameDB.sqlite < Queries/Query#.sql

To Run web app:
1. bash
2. cd app
3. python3 app.py
4. Click on link to server