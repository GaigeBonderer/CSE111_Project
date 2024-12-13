// Add an event listener to the action dropdown
document.getElementById("action").addEventListener("change", function () {
    const action = this.value; // Get the selected action
    console.log("Selected action:", action); // Log the selected action for testing
    const formFields = document.getElementById("form-fields"); // Get the form fields container

    // Clear any previously added fields
    formFields.innerHTML = "";

    // Add input fields dynamically based on the selected action
    if (action === "guild_members" || action === "specific_guild") {
        // Input field for guild-related actions
        console.log("Adding Guild Name input field"); // Log for testing
        formFields.innerHTML = `
            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" placeholder="Case Sensitive">
        `;
    } else if (action === "clan_members" || action === "specific_clan") {
        // Input field for clan-related actions
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
        // Input field for entity-related actions
        formFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID">
        `;
    } else if (action === "specific_weapon") {
        // Input field for weapon-related actions
        formFields.innerHTML = `
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID">
        `;
    }
});


