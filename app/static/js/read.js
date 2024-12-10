document.getElementById("action").addEventListener("change", function () {
    const action = this.value;
    console.log("Selected action:", action); // testing
    const formFields = document.getElementById("form-fields");

    // Clear previous fields
    formFields.innerHTML = "";

    // Add fields based on the selected action
    if (action === "guild_members" || action === "specific_guild") {
        console.log("Adding Guild Name input field"); // testing
        formFields.innerHTML = `
            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" placeholder="Case Sensitive">
        `;
    } else if (action === "clan_members" || action === "specific_clan") {
        formFields.innerHTML = `
            <label for="clanName">Clan Name:</label>
            <input type="text" id="clanName" name="clanName" placeholder="Case Sensitive">
        `;
    } else if (
        action === "specific_entity" ||
        action === "player_inventory" ||
        action === "enemy_can_drop" ||
        action === "entity_equipped_weapon"
    ) {
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID">
        `;
    } else if (action === "specific_weapon") {
        formFields.innerHTML = `
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID">
        `;
    }
});

