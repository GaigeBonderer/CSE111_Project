from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'weapon'



def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')




@app.route('/')
def home():
    return render_template('login.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')




@app.route('/portal')
def admin_page():
    return render_template('portal.html')




@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))




@app.route('/read')
def read_page():
    return render_template('read.html')




@app.route('/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        table = request.form.get('table')

        conn = get_db_connection()
        cursor = conn.cursor()

        if table == "Player":
            username = request.form.get('username')
            gender = request.form.get('gender')

            # type = request.form.get('type')
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')

            # Add to Entity table
            cursor.execute("""
                INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('P', atk, defe, lvl, spd, chp, thp))
            entity_id = cursor.lastrowid

            # Add to Player table
            cursor.execute("""
                INSERT INTO Player (EntityID, Gender, Username)
                VALUES (?, ?, ?)
            """, (entity_id, gender, username))

        elif table == "Enemy":
            name = request.form.get('name')
            is_boss = request.form.get('isBoss')

            # type = request.form.get('type')
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')

            # Add to Entity table
            cursor.execute("""
                INSERT INTO Entity (Type, Attack, Defense, Level, Speed, CurrentHP, TotalHP)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('E', atk, defe, lvl, spd, chp, thp))
            entity_id = cursor.lastrowid

            # Add to Enemy table
            cursor.execute("""
                INSERT INTO Enemy (EntityID, Name, IsBoss)
                VALUES (?, ?, ?)
            """, (entity_id, name, is_boss))

        elif table == "Weapon":
            desc = request.form.get('desc')
            rank = request.form.get('rank')
            type = request.form.get('type')
            name = request.form.get('name')
            special = request.form.get('special')
            damage = request.form.get('damage')
            atkspeed = request.form.get('atkspeed')
            range = request.form.get('range')

            cursor.execute("""
                INSERT INTO Weapon (Description, Rank, Type, Name, SpecialATR, Damage, ATKSpeed, Range)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (desc, rank, type, name, special, damage, atkspeed, range))

        elif table == "Guild":
            guild_name = request.form.get('guildName')
            guild_bonus = request.form.get('guildBonus')

            cursor.execute("""
                INSERT INTO Guild (GuildName, GuildBonus, TotalPlayers)
                VALUES (?, ?, ?)
            """, (guild_name, guild_bonus, 0))

        elif table == "Clan":
            clan_name = request.form.get('clanName')
            clan_bonus = request.form.get('clanBonus')
            boss_name = request.form.get('bossName')

            cursor.execute("""
                INSERT INTO Clan (ClanName, ClanBonus, BossName)
                VALUES (?, ?, ?)
            """, (clan_name, clan_bonus, boss_name))

        conn.commit()
        conn.close()
        return redirect(url_for('create_page'))

    return render_template('create.html')






@app.route('/delete')
def delete_page():
    return render_template('delete.html')





@app.route('/update')
def update_page():
    return render_template('update.html')





if __name__ == '__main__':
    app.run(debug=True)
