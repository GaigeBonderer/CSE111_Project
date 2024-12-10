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






@app.route('/delete', methods=['GET', 'POST'])
def delete_page():
    if request.method == 'POST':
        action = request.form.get('action')
        entity_id = request.form.get('entityID')
        table_name = request.form.get('tableName')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete from respective table
        if action == "delete_player":
            entity_id = request.form.get('entityID')

            # Fetch the player's guild (if any)
            cursor.execute("""
                SELECT GuildName FROM PlayerBelongs WHERE EntityID = ?
            """, (entity_id,))
            guild_name = cursor.fetchone()

            # Delete from PlayerBelongs
            cursor.execute("DELETE FROM PlayerBelongs WHERE EntityID = ?", (entity_id,))

            # If the player in a guild -1 TotalPlayers
            if guild_name:
                cursor.execute("""
                    UPDATE Guild
                    SET TotalPlayers = TotalPlayers - 1
                    WHERE GuildName = ?
                """, (guild_name[0],))

            # Delete from Equipped
            cursor.execute("DELETE FROM Equipped WHERE EntityID = ?", (entity_id,))

            # Delete from Inventory
            cursor.execute("DELETE FROM Inventory WHERE EntityID = ?", (entity_id,))

            # Delete from Player table
            cursor.execute("DELETE FROM Player WHERE EntityID = ?", (entity_id,))

            # Delete from Entity table
            cursor.execute("DELETE FROM Entity WHERE EntityID = ?", (entity_id,))



        elif action == "delete_enemy":
            entity_id = request.form.get('entityID')

            # Delete from EnemyBelongs
            cursor.execute("DELETE FROM EnemyBelongs WHERE EntityID = ?", (entity_id,))

            # Delete from CanDrop
            cursor.execute("DELETE FROM CanDrop WHERE EntityID = ?", (entity_id,))

            # Delete from Equipped
            cursor.execute("DELETE FROM Equipped WHERE EntityID = ?", (entity_id,))

            # Delete from Enemy table
            cursor.execute("DELETE FROM Enemy WHERE EntityID = ?", (entity_id,))

            # Delete from Entity table
            cursor.execute("DELETE FROM Entity WHERE EntityID = ?", (entity_id,))

            print(f"Enemy with EntityID {entity_id} and all related entries deleted.")


        elif action == "delete_clan":
            clan_name = request.form.get('clanName')
            cursor.execute("DELETE FROM Clan WHERE ClanName = ?", (clan_name,))
            cursor.execute("DELETE FROM EnemyBelongs WHERE ClanName = ?", (clan_name,))
            print(f"Clan '{clan_name}' and related entries deleted.")

        elif action == "delete_guild":
            guild_name = request.form.get('guildName')
            cursor.execute("DELETE FROM Guild WHERE GuildName = ?", (guild_name,))
            cursor.execute("DELETE FROM PlayerBelongs WHERE GuildName = ?", (guild_name,))
            print(f"Guild '{guild_name}' and related entries deleted.")

        elif action == "delete_weapon":
            weapon_id = request.form.get('weaponID')
            cursor.execute("DELETE FROM Weapon WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM Inventory WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM Equipped WHERE WeaponID = ?", (weapon_id,))
            cursor.execute("DELETE FROM CanDrop WHERE WeaponID = ?", (weapon_id,))
            print(f"Weapon with WeaponID {weapon_id} and related entries deleted.")

        conn.commit()
        conn.close()

    return render_template('delete.html')






@app.route('/update', methods=['GET', 'POST'])
def update_page():
    if request.method == 'POST':
        action = request.form.get('action')
        conn = get_db_connection()
        cursor = conn.cursor()

        if action == "update_player":
            entity_id = request.form.get('entityID')
            
            # Entity attributes
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')
            
            # Player-specific attributes
            username = request.form.get('username')
            gender = request.form.get('gender')

            # Build dynamic query for Entity table
            entity_update_fields = []
            entity_update_values = []

            if atk:
                entity_update_fields.append("Attack = ?")
                entity_update_values.append(atk)
            if defe:
                entity_update_fields.append("Defense = ?")
                entity_update_values.append(defe)
            if lvl:
                entity_update_fields.append("Level = ?")
                entity_update_values.append(lvl)
            if spd:
                entity_update_fields.append("Speed = ?")
                entity_update_values.append(spd)
            if chp:
                entity_update_fields.append("CurrentHP = ?")
                entity_update_values.append(chp)
            if thp:
                entity_update_fields.append("TotalHP = ?")
                entity_update_values.append(thp)

            if entity_update_fields:
                entity_update_values.append(entity_id)
                entity_update_query = f"""
                    UPDATE Entity
                    SET {', '.join(entity_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(entity_update_query, tuple(entity_update_values))

            # Build dynamic query for Player table
            player_update_fields = []
            player_update_values = []

            if username:
                player_update_fields.append("Username = ?")
                player_update_values.append(username)
            if gender:
                player_update_fields.append("Gender = ?")
                player_update_values.append(gender)

            if player_update_fields:
                player_update_values.append(entity_id)
                player_update_query = f"""
                    UPDATE Player
                    SET {', '.join(player_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(player_update_query, tuple(player_update_values))

            conn.commit()

        elif action == "update_enemy":
            entity_id = request.form.get('entityID')
            
            # Entity attributes
            atk = request.form.get('atk')
            defe = request.form.get('defe')
            lvl = request.form.get('lvl')
            spd = request.form.get('spd')
            chp = request.form.get('chp')
            thp = request.form.get('thp')
            
            # Enemy-specific attributes
            name = request.form.get('name')
            is_boss = request.form.get('isBoss')

            # Build dynamic query for Entity table
            entity_update_fields = []
            entity_update_values = []

            if atk:
                entity_update_fields.append("Attack = ?")
                entity_update_values.append(atk)
            if defe:
                entity_update_fields.append("Defense = ?")
                entity_update_values.append(defe)
            if lvl:
                entity_update_fields.append("Level = ?")
                entity_update_values.append(lvl)
            if spd:
                entity_update_fields.append("Speed = ?")
                entity_update_values.append(spd)
            if chp:
                entity_update_fields.append("CurrentHP = ?")
                entity_update_values.append(chp)
            if thp:
                entity_update_fields.append("TotalHP = ?")
                entity_update_values.append(thp)

            if entity_update_fields:
                entity_update_values.append(entity_id)
                entity_update_query = f"""
                    UPDATE Entity
                    SET {', '.join(entity_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(entity_update_query, tuple(entity_update_values))

            # Build dynamic query for Enemy table
            enemy_update_fields = []
            enemy_update_values = []

            if name:
                enemy_update_fields.append("Name = ?")
                enemy_update_values.append(name)
            if is_boss:
                enemy_update_fields.append("IsBoss = ?")
                enemy_update_values.append(is_boss)

            if enemy_update_fields:
                enemy_update_values.append(entity_id)
                enemy_update_query = f"""
                    UPDATE Enemy
                    SET {', '.join(enemy_update_fields)}
                    WHERE EntityID = ?
                """
                cursor.execute(enemy_update_query, tuple(enemy_update_values))

            conn.commit()

        elif action == "assign_player_guild":
            entity_id = request.form.get('entityID')
            new_guild_name = request.form.get('guildName')

            # Check if Player is already in a guild
            cursor.execute("""
                SELECT GuildName
                FROM PlayerBelongs
                WHERE EntityID = ?
            """, (entity_id,))
            current_guild = cursor.fetchone()

            # If in another guild decrease total player count
            if current_guild:
                previous_guild_name = current_guild[0]
                cursor.execute("""
                    UPDATE Guild
                    SET TotalPlayers = TotalPlayers - 1
                    WHERE GuildName = ?
                """, (previous_guild_name,))

                # Delete player belongs for previous guild
                cursor.execute("""
                    DELETE FROM PlayerBelongs
                    WHERE EntityID = ? AND GuildName = ?
                """, (entity_id, previous_guild_name))

            # Assign player to new guild
            cursor.execute("""
                INSERT OR REPLACE INTO PlayerBelongs (EntityID, GuildName)
                VALUES (?, ?)
            """, (entity_id, new_guild_name))

            # Increase total player count for new guild
            cursor.execute("""
                UPDATE Guild
                SET TotalPlayers = TotalPlayers + 1
                WHERE GuildName = ?
            """, (new_guild_name,))

        elif action == "assign_enemy_clan":
            entity_id = request.form.get('entityID')
            new_clan_name = request.form.get('clanName')

            cursor.execute("""
                SELECT ClanName
                FROM EnemyBelongs
                WHERE EntityID = ?
            """, (entity_id,))
            current_clan = cursor.fetchone()

            if current_clan:
                current_clan_name = current_clan[0]
                if current_clan_name != new_clan_name:
                    cursor.execute("""
                        DELETE FROM EnemyBelongs
                        WHERE EntityID = ? AND ClanName = ?
                    """, (entity_id, current_clan_name))
                    print(f"Removed Entity {entity_id} from Clan {current_clan_name}")

            cursor.execute("""
                INSERT OR REPLACE INTO EnemyBelongs (EntityID, ClanName)
                VALUES (?, ?)
            """, (entity_id, new_clan_name))
            print(f"Assigned Entity {entity_id} to Clan {new_clan_name}")

            conn.commit()

        elif action == "update_weapon":
            weaponID = request.form.get('weaponID')
            desc = request.form.get('desc')
            rank = request.form.get('rank')
            type = request.form.get('type')
            name = request.form.get('name')
            special = request.form.get('special')
            damage = request.form.get('damage')
            atkspeed = request.form.get('atkspeed')
            range = request.form.get('range')

            update_fields = []
            update_values = []

            # Dynamically build update*TM
            if desc:
                update_fields.append("Description = ?")
                update_values.append(desc)
            if rank:
                update_fields.append("Rank = ?")
                update_values.append(rank)
            if type:
                update_fields.append("Type = ?")
                update_values.append(type)
            if name:
                update_fields.append("Name = ?")
                update_values.append(name)
            if special:
                update_fields.append("SpecialATR = ?")
                update_values.append(special)
            if damage:
                update_fields.append("Damage = ?")
                update_values.append(damage)
            if atkspeed:
                update_fields.append("ATKSpeed = ?")
                update_values.append(atkspeed)
            if range:
                update_fields.append("Range = ?")
                update_values.append(range)

            if update_fields:
                update_values.append(weaponID)

                update_query = f"""
                    UPDATE Weapon
                    SET {', '.join(update_fields)}
                    WHERE WeaponID = ?
                """

                cursor.execute(update_query, tuple(update_values))
                conn.commit()

        elif action == "update_guild":
            old_guild_name = request.form.get('oldGuildName')
            new_guild_name = request.form.get('newGuildName')
            guild_bonus = request.form.get('guildBonus')
            total_players = request.form.get('totalPlayers')

            update_guild_query = "UPDATE Guild SET "
            update_values = []
            update_fields = []

            if new_guild_name:
                update_fields.append("GuildName = ?")
                update_values.append(new_guild_name)
            if guild_bonus:
                update_fields.append("GuildBonus = ?")
                update_values.append(guild_bonus)
            if total_players:
                update_fields.append("TotalPlayers = ?")
                update_values.append(total_players)

            if update_fields:
                update_guild_query += ", ".join(update_fields) + " WHERE GuildName = ?"
                update_values.append(old_guild_name)

                cursor.execute(update_guild_query, update_values)
                print(f"Guild '{old_guild_name}' updated successfully.")

            # If the guild name is updated, update PlayerBelongs table
            if new_guild_name:
                cursor.execute("""
                    UPDATE PlayerBelongs
                    SET GuildName = ?
                    WHERE GuildName = ?
                """, (new_guild_name, old_guild_name))
                print(f"PlayerBelongs table updated to new GuildName '{new_guild_name}'.")

            conn.commit()


        elif action == "update_clan":
            old_clan_name = request.form.get('oldClanName')
            new_clan_name = request.form.get('newClanName')
            clan_bonus = request.form.get('clanBonus')
            boss_name = request.form.get('bossName')

            update_clan_query = "UPDATE Clan SET "
            update_values = []
            update_fields = []

            if new_clan_name:
                update_fields.append("ClanName = ?")
                update_values.append(new_clan_name)
            if clan_bonus:
                update_fields.append("ClanBonus = ?")
                update_values.append(clan_bonus)
            if boss_name:
                update_fields.append("BossName = ?")
                update_values.append(boss_name)

            if update_fields:
                update_clan_query += ", ".join(update_fields) + " WHERE ClanName = ?"
                update_values.append(old_clan_name)

                cursor.execute(update_clan_query, update_values)
                print(f"Clan '{old_clan_name}' updated successfully.")

            # If the clan name updated, update EnemyBelongs table as well
            if new_clan_name:
                cursor.execute("""
                    UPDATE EnemyBelongs
                    SET ClanName = ?
                    WHERE ClanName = ?
                """, (new_clan_name, old_clan_name))
                print(f"EnemyBelongs table updated to new ClanName '{new_clan_name}'.")

            conn.commit()


        
        elif action == "assign_weapon_equipped":
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT EntityID 
                FROM Entity 
                WHERE EntityID = ?
            """, (entity_id,))
            entity_exists = cursor.fetchone()

            cursor.execute("""
                SELECT WeaponID 
                FROM Weapon 
                WHERE WeaponID = ?
            """, (weapon_id,))
            weapon_exists = cursor.fetchone()

            if not entity_exists:
                conn.close()
                return render_template('read.html', message=f"Entity with ID {entity_id} does not exist.", column_names=None, data=None)

            if not weapon_exists:
                conn.close()
                return render_template('read.html', message=f"Weapon with ID {weapon_id} does not exist.", column_names=None, data=None)

            cursor.execute("""
                SELECT * 
                FROM Equipped 
                WHERE WeaponID = ?
            """, (weapon_id,))
            already_equipped = cursor.fetchone()

            if already_equipped:
                conn.close()
                return render_template('read.html', message=f"Weapon with ID {weapon_id} is already equipped by another entity.", column_names=None, data=None)

            cursor.execute("""
                SELECT WeaponID 
                FROM Equipped 
                WHERE EntityID = ?
            """, (entity_id,))
            currently_equipped = cursor.fetchone()

            if currently_equipped:
                cursor.execute("""
                    DELETE FROM Equipped 
                    WHERE EntityID = ?
                """, (entity_id,))

            cursor.execute("""
                INSERT INTO Equipped (EntityID, WeaponID)
                VALUES (?, ?)
            """, (entity_id, weapon_id))

            conn.commit()
            conn.close()

            return render_template('read.html', message=f"Weapon with ID {weapon_id} successfully equipped to Entity with ID {entity_id}.", column_names=None, data=None)

    

        elif action == "assign_weapon_inventory":
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # checks if weapon is in entity's inventory
            cursor.execute("""
                SELECT 1 
                FROM Inventory
                WHERE EntityID = ? AND WeaponID = ?
            """, (entity_id, weapon_id))
            result = cursor.fetchone()

            if result:
                message = f"Weapon ID {weapon_id} is already in the inventory of Entity ID {entity_id}."
            else:
                cursor.execute("""
                    INSERT INTO Inventory (EntityID, WeaponID)
                    VALUES (?, ?)
                """, (entity_id, weapon_id))
                conn.commit()

                message = f"Weapon ID {weapon_id} successfully added to the inventory of Entity ID {entity_id}."

            conn.close()
            return render_template('read.html', message=message)

        

        elif action == "assign_weapon_candrop":
            entity_id = request.form.get('entityID')
            weapon_id = request.form.get('weaponID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1 
                FROM CanDrop
                WHERE EntityID = ? AND WeaponID = ?
            """, (entity_id, weapon_id))
            result = cursor.fetchone()

            if result:
                message = f"Weapon ID {weapon_id} is already in the CanDrop list for Entity ID {entity_id}."
            else:
                cursor.execute("""
                    INSERT INTO CanDrop (EntityID, WeaponID)
                    VALUES (?, ?)
                """, (entity_id, weapon_id))
                conn.commit()
                message = f"Weapon ID {weapon_id} successfully added to the CanDrop list for Entity ID {entity_id}."

            conn.close()
            return render_template('read.html', message=message)

            

        

        conn.commit()
        conn.close()
        return redirect(url_for('update_page'))

    return render_template('update.html')



@app.route('/read', methods=['GET', 'POST'])
def read_page():
    column_names = []
    data = []

    if request.method == 'POST':
        action = request.form.get('action')

        conn = get_db_connection()
        cursor = conn.cursor()

        if action == "all_players":

            print("all_players CALLED")

            cursor.execute("""
                SELECT 
                    p.EntityID AS 'Entity ID',
                    p.Username AS 'Username',
                    p.Gender AS 'Gender',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP'
                FROM 
                    Player p
                INNER JOIN 
                    Entity e 
                ON 
                    p.EntityID = e.EntityID
                ORDER BY 
                    p.EntityID ASC
            """)
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            print(column_names)

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "all_enemies":
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    e.EntityID AS 'Entity ID',
                    en.Name AS 'Name',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    en.IsBoss AS 'Is Boss'
                FROM 
                    Enemy en
                INNER JOIN 
                    Entity e 
                ON 
                    en.EntityID = e.EntityID
                ORDER BY 
                    e.EntityID ASC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)

        elif action == "all_guilds":
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    GuildName AS 'Guild Name',
                    GuildBonus AS 'Guild Bonus',
                    TotalPlayers AS 'Total Players'
                FROM 
                    Guild
                ORDER BY 
                    TotalPlayers DESC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)
        
        elif action == "all_clans":
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    ClanName AS 'Clan Name',
                    ClanBonus AS 'Clan Bonus',
                    BossName AS 'Boss Name'
                FROM 
                    Clan
                ORDER BY 
                    ClanName ASC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)

        
        elif action == "all_weapons":
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    WeaponID AS 'Weapon ID',
                    Name AS 'Name',
                    Type AS 'Type',
                    Rank AS 'Rank',
                    Damage AS 'Damage',
                    ATKSpeed AS 'Attack Speed',
                    Range AS 'Range',
                    SpecialATR AS 'Special Attribute',
                    Description AS 'Description'
                FROM 
                    Weapon
                ORDER BY 
                    WeaponID ASC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "guild_members":
            guild_name = request.form.get('guildName')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    pb.GuildName AS 'Guild Name',
                    p.EntityID AS 'Entity ID',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    p.Username AS 'Username',
                    p.Gender AS 'Gender'
                FROM 
                    PlayerBelongs pb
                INNER JOIN 
                    Player p ON pb.EntityID = p.EntityID
                INNER JOIN 
                    Entity e ON p.EntityID = e.EntityID
                WHERE 
                    pb.GuildName = ?
                ORDER BY 
                    e.Level DESC
            """, (guild_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "clan_members":
            clan_name = request.form.get('clanName')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    c.ClanName AS 'Clan Name',
                    e.Level AS 'Level',
                    e.Attack AS 'Attack',
                    e.Defense AS 'Defense',
                    e.Speed AS 'Speed',
                    e.CurrentHP AS 'Current HP',
                    e.TotalHP AS 'Total HP',
                    en.Name AS 'Enemy Name',
                    en.IsBoss AS 'Is Boss'
                FROM 
                    Clan c
                INNER JOIN 
                    EnemyBelongs eb ON c.ClanName = eb.ClanName
                INNER JOIN 
                    Enemy en ON eb.EntityID = en.EntityID
                INNER JOIN 
                    Entity e ON en.EntityID = e.EntityID
                WHERE 
                    c.ClanName = ?
                ORDER BY 
                    e.Level DESC
            """, (clan_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "specific_entity":

            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            # Determine entity type
            cursor.execute("SELECT Type FROM Entity WHERE EntityID = ?", (entity_id,))
            result = cursor.fetchone()

            entity_type = result[0]

            if entity_type == 'P':
                cursor.execute("""
                    SELECT 
                        e.EntityID AS 'Entity ID',
                        p.Username AS 'Username',
                        e.Level AS 'Level',
                        e.Attack AS 'Attack',
                        e.Defense AS 'Defense',
                        e.Speed AS 'Speed',
                        e.CurrentHP AS 'Current HP',
                        e.TotalHP AS 'Total HP',
                        p.Gender AS 'Gender'
                    FROM 
                        Entity e
                    INNER JOIN 
                        Player p ON e.EntityID = p.EntityID
                    WHERE 
                        e.EntityID = ?
                """, (entity_id,))


            elif entity_type == 'E':
                cursor.execute("""
                    SELECT 
                        e.EntityID AS 'Entity ID',
                        en.Name AS 'Enemy Name',
                        e.Level AS 'Level',
                        e.Attack AS 'Attack',
                        e.Defense AS 'Defense',
                        e.Speed AS 'Speed',
                        e.CurrentHP AS 'Current HP',
                        e.TotalHP AS 'Total HP',
                        en.IsBoss AS 'Is Boss'
                    FROM 
                        Entity e
                    INNER JOIN 
                        Enemy en ON e.EntityID = en.EntityID
                    WHERE 
                        e.EntityID = ?
                """, (entity_id,))
            else:
                # Handle unexpected type
                return render_template('read.html', column_names=[], data=[], error=f"Unexpected entity type for ID {entity_id}.")

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "specific_weapon":
            weapon_id = request.form.get('weaponID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    WeaponID AS 'Weapon ID',
                    Name AS 'Weapon Name',
                    Type AS 'Type',
                    Rank AS 'Rank',
                    Description AS 'Description',
                    SpecialATR AS 'Special Attribute',
                    Damage AS 'Damage',
                    ATKSpeed AS 'Attack Speed',
                    Range AS 'Range'
                FROM 
                    Weapon
                WHERE 
                    WeaponID = ?
            """, (weapon_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "specific_guild":
            guild_name = request.form.get('guildName')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    GuildName AS 'Guild Name',
                    GuildBonus AS 'Guild Bonus',
                    TotalPlayers AS 'Total Players'
                FROM 
                    Guild
                WHERE 
                    GuildName = ?
            """, (guild_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "specific_clan":
            clan_name = request.form.get('clanName')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    ClanName AS 'Clan Name',
                    ClanBonus AS 'Clan Bonus',
                    BossName AS 'Boss Name'
                FROM 
                    Clan
                WHERE 
                    ClanName = ?
            """, (clan_name,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "player_inventory":
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    p.Username AS 'Player Name',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    Inventory i
                INNER JOIN 
                    Weapon w ON i.WeaponID = w.WeaponID
                INNER JOIN 
                    Player p ON i.EntityID = p.EntityID
                WHERE 
                    i.EntityID = ?
                ORDER BY 
                    w.Rank ASC
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)


        elif action == "enemy_can_drop":
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    e.Name AS 'Enemy Name',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    CanDrop c
                INNER JOIN 
                    Weapon w ON c.WeaponID = w.WeaponID
                INNER JOIN 
                    Enemy e ON c.EntityID = e.EntityID
                WHERE 
                    c.EntityID = ?
                ORDER BY 
                    w.Rank ASC
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)
        

        elif action == "entity_equipped_weapon":
            entity_id = request.form.get('entityID')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN p.EntityID IS NOT NULL THEN p.Username
                        WHEN e.EntityID IS NOT NULL THEN e.Name
                        ELSE 'Unknown'
                    END AS 'Entity Name',
                    CASE 
                        WHEN p.EntityID IS NOT NULL THEN 'Player'
                        WHEN e.EntityID IS NOT NULL THEN 'Enemy'
                        ELSE 'Unknown'
                    END AS 'Entity Type',
                    w.Name AS 'Weapon Name',
                    w.Description AS 'Description',
                    w.Rank AS 'Rarity',
                    w.Type AS 'Type',
                    w.SpecialATR AS 'Special Attribute',
                    w.Damage AS 'Damage',
                    w.ATKSpeed AS 'Attack Speed',
                    w.Range AS 'Range'
                FROM 
                    Equipped eq
                INNER JOIN 
                    Weapon w ON eq.WeaponID = w.WeaponID
                LEFT JOIN 
                    Player p ON eq.EntityID = p.EntityID
                LEFT JOIN 
                    Enemy e ON eq.EntityID = e.EntityID
                WHERE 
                    eq.EntityID = ?
            """, (entity_id,))

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)



        elif action == "weapon_type_avg":
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    Type AS 'Weapon Type',
                    ROUND(AVG(Damage), 1) AS 'Average Damage',
                    ROUND(AVG(ATKSpeed), 1) AS 'Average Attack Speed',
                    ROUND(AVG(Range), 1) AS 'Average Range',
                    ROUND((AVG(Damage) + AVG(ATKSpeed) + AVG(Range)), 1) AS 'Average Total'
                FROM 
                    Weapon
                WHERE 
                    Rank = 'Common'
                GROUP BY 
                    Type
                ORDER BY 
                    ROUND((AVG(Damage) + AVG(ATKSpeed) + AVG(Range)), 1) ASC
            """)

            # Fetch column names and data
            column_names = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            conn.close()

            # Render template with data and column names
            return render_template('read.html', column_names=column_names, data=data)




        return render_template('read.html', data=data)

    return render_template('read.html', column_names=column_names, data=data)



if __name__ == '__main__':
    app.run(debug=True)
