// Add an event listener to the action dropdown
document.getElementById("action").addEventListener("change", (event) => {
    const action = event.target.value; // Get the selected action
    const deleteFields = document.getElementById("delete-fields"); // Get the container for delete fields

    // Clear any previously added fields
    deleteFields.innerHTML = "";

    // Add input fields dynamically based on the selected action
    if (action === "delete_player" || action === "delete_enemy") {
        // Input field for deleting a player or enemy
        deleteFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID" placeholder="Enter Entity ID" required>
        `;
    } else if (action === "delete_clan") {
        // Input field for deleting a clan
        deleteFields.innerHTML = `
            <label for="clanName">Clan Name:</label>
            <input type="text" id="clanName" name="clanName" placeholder="Enter Clan Name" required>
        `;
    } else if (action === "delete_guild") {
        // Input field for deleting a guild
        deleteFields.innerHTML = `
            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" placeholder="Enter Guild Name" required>
        `;
    } else if (action === "delete_weapon") {
        // Input field for deleting a weapon
        deleteFields.innerHTML = `
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID" placeholder="Enter Weapon ID" required>
        `;
    }
});

