// Add an event listener to the table selection dropdown
document.getElementById("table-select").addEventListener("change", function () {
    const table = this.value; // Get the selected table value
    const formFields = document.getElementById("form-fields"); // Get the form fields container

    formFields.innerHTML = ""; // Clear any existing fields

    // Populate form fields based on the selected table
    if (table === "Player") {
        // Player-specific form fields
        formFields.innerHTML = `
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>

            <label for="gender">Gender:</label>
            <select id="gender" name="gender" required>
                <option value="M">Male</option>
                <option value="F">Female</option>
            </select>

            <label for="name">Attack:</label>
            <input type="number" id="atk" name="atk" required>

            <label for="name">Defense:</label>
            <input type="number" id="defe" name="defe" required>
            
            <label for="name">Level:</label>
            <input type="number" id="lvl" name="lvl" required>

            <label for="name">Speed:</label>
            <input type="number" id="spd" name="spd" required>

            <label for="name">Current HP:</label>
            <input type="number" id="chp" name="chp" required>

            <label for="name">Total HP:</label>
            <input type="number" id="thp" name="thp" required>
        `;
    } else if (table === "Enemy") {
        // Enemy-specific form fields
        formFields.innerHTML = `
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="isBoss">Is Boss:</label>
            <select id="isBoss" name="isBoss" required>
                <option value="1">Yes</option>
                <option value="0">No</option>
            </select>

            <label for="name">Attack:</label>
            <input type="number" id="atk" name="atk" required>

            <label for="name">Defense:</label>
            <input type="number" id="defe" name="defe" required>
            
            <label for="name">Level:</label>
            <input type="number" id="lvl" name="lvl" required>

            <label for="name">Speed:</label>
            <input type="number" id="spd" name="spd" required>

            <label for="name">Current HP:</label>
            <input type="number" id="chp" name="chp" required>

            <label for="name">Total HP:</label>
            <input type="number" id="thp" name="thp" required>
        `;
    } else if (table === "Weapon") {
        // Weapon-specific form fields
        formFields.innerHTML = `
            <label for="name">Description:</label>
            <input type="text" id="desc" name="desc" required>

            <label for="name">Rank:</label>
            <input type="text" id="rank" name="rank" required>

            <label for="name">Type:</label>
            <input type="text" id="type" name="type" required>

            <label for="name">Weapon Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="name">Special Attribute:</label>
            <input type="text" id="special" name="special" required>

            <label for="damage">Damage:</label>
            <input type="number" id="damage" name="damage" required>

            <label for="name">Attack speed:</label>
            <input type="number" id="atkspeed" name="atkspeed" required>

            <label for="range">Range:</label>
            <input type="number" id="range" name="range" required>
        `;
    } else if (table === "Guild") {
        // Guild-specific form fields
        formFields.innerHTML = `
            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" required>

            <label for="guildBonus">Guild Bonus:</label>
            <input type="text" id="guildBonus" name="guildBonus" required>
        `;
    } else if (table === "Clan") {
        // Clan-specific form fields
        formFields.innerHTML = `
            <label for="clanName">Clan Name:</label>
            <input type="text" id="clanName" name="clanName" required>

            <label for="clanBonus">Clan Bonus:</label>
            <input type="text" id="clanBonus" name="clanBonus" required>

            <label for="bossName">Boss Name:</label>
            <input type="text" id="bossName" name="bossName" required>
        `;
    }
});

