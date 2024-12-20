// Add an event listener to the update action dropdown
document.getElementById("update-select").addEventListener("change", function () {
    const action = this.value; // Get the selected action
    const formFields = document.getElementById("form-fields"); // Get the form fields container

    formFields.innerHTML = ""; // Clear any existing form fields

    if (action === "update_player") {
        // Fields for updating a player
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="number" id="entityID" name="entityID" required>

            <label for="username">New Username (optional):</label>
            <input type="text" id="username" name="username">

            <label for="gender">New Gender:</label>
            <select id="gender" name="gender" required>
                <option value="M">Male</option>
                <option value="F">Female</option>
            </select>

            <label for="name">New Attack (optional):</label>
            <input type="number" id="atk" name="atk">

            <label for="name">New Defense (optional):</label>
            <input type="number" id="defe" name="defe">
            
            <label for="name">New Level (optional):</label>
            <input type="number" id="lvl" name="lvl">

            <label for="name">New Speed (optional):</label>
            <input type="number" id="spd" name="spd">

            <label for="name">New Current HP (optional):</label>
            <input type="number" id="chp" name="chp">

            <label for="name">New Total HP (optional):</label>
            <input type="number" id="thp" name="thp">
        `;
    } else if (action === "update_enemy") {
        // Fields for updating an enemy
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="number" id="entityID" name="entityID" required>

            <label for="name">New Name (optional):</label>
            <input type="text" id="name" name="name">

            <label for="isBoss">Is Boss:</label>
            <select id="isBoss" name="isBoss" required>
                <option value="1">Yes</option>
                <option value="0">No</option>
            </select>

            <label for="name">New Attack (optional):</label>
            <input type="number" id="atk" name="atk">

            <label for="name">New Defense (optional):</label>
            <input type="number" id="defe" name="defe">
            
            <label for="name">New Level (optional):</label>
            <input type="number" id="lvl" name="lvl">

            <label for="name">New Speed (optional):</label>
            <input type="number" id="spd" name="spd">

            <label for="name">New Current HP (optional):</label>
            <input type="number" id="chp" name="chp">

            <label for="name">New Total HP (optional):</label>
            <input type="number" id="thp" name="thp">
        `;
    } else if (action === "assign_player_guild") {
        // Fields for assigning a player to a guild
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="number" id="entityID" name="entityID" required>

            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" required>
        `;
    } else if (action === "assign_enemy_clan") {
        // Fields for assigning an enemy to a clan
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="number" id="entityID" name="entityID" required>

            <label for="clanName">Clan Name:</label>
            <input type="text" id="clanName" name="clanName" required>
        `;
    } else if (action === "update_weapon") {
        // Fields for updating a weapon
        formFields.innerHTML = `
            <label for="weaponID">Weapon ID:</label>
            <input type="number" id="weaponID" name="weaponID" required>

            <label for="name">New Description (optional):</label>
            <input type="text" id="desc" name="desc">

            <label for="name">New Rank (optional):</label>
            <input type="text" id="rank" name="rank">

            <label for="name">New Type (optional):</label>
            <input type="text" id="type" name="type">

            <label for="name">New Name (optional):</label>
            <input type="text" id="name" name="name">

            <label for="name">New Special Attribute (optional):</label>
            <input type="text" id="special" name="special">

            <label for="damage">New Damage (optional):</label>
            <input type="number" id="damage" name="damage">

            <label for="name">New Attack speed (optional):</label>
            <input type="number" id="atkspeed" name="atkspeed">

            <label for="range">New Range (optional):</label>
            <input type="number" id="range" name="range">
        `;
    } else if (action === "update_guild") {
        // Fields for updating a guild
        formFields.innerHTML = `
            <label for="oldGuildName">Current Guild Name:</label>
            <input type="text" id="oldGuildName" name="oldGuildName" placeholder="Enter current guild name" required>
    
            <label for="newGuildName">New Guild Name (optional):</label>
            <input type="text" id="newGuildName" name="newGuildName">
    
            <label for="guildBonus">Guild Bonus (optional):</label>
            <input type="text" id="guildBonus" name="guildBonus">
    
            <label for="totalPlayers">Total Players (optional):</label>
            <input type="number" id="totalPlayers" name="totalPlayers">
        `;
    } else if (action === "update_clan") {
        // Fields for updating a clan
        formFields.innerHTML = `
            <label for="oldClanName">Current Clan Name:</label>
            <input type="text" id="oldClanName" name="oldClanName" placeholder="Enter current clan name" required>
    
            <label for="newClanName">New Clan Name (optional):</label>
            <input type="text" id="newClanName" name="newClanName">
    
            <label for="clanBonus">Clan Bonus (optional):</label>
            <input type="text" id="clanBonus" name="clanBonus">
    
            <label for="bossName">Boss Name (optional):</label>
            <input type="text" id="bossName" name="bossName">
        `;
    } else if (action === "assign_weapon_equipped") {
        // Fields for assigning a weapon to an entity
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID" required>
        
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID" required>
        `;
    } else if (action === "assign_weapon_inventory") {
        // Fields for adding a weapon to an entity's inventory
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID" required>
        
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID" required>
        `;
    } else if (action === "assign_weapon_candrop") {
        // Fields for marking a weapon as droppable by an entity
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID" required>
        
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID" required>
        `;
    }
});

