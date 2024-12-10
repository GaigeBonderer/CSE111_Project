document.getElementById("action").addEventListener("change", (event) => {
    const action = event.target.value;
    const deleteFields = document.getElementById("delete-fields");

    // Clear previous fields
    deleteFields.innerHTML = "";

    if (action === "delete_player" || action === "delete_enemy") {
        deleteFields.innerHTML = `
            <label for="entityID">Entity ID:</label>
            <input type="text" id="entityID" name="entityID" placeholder="Enter Entity ID" required>
        `;
    } else if (action === "delete_clan") {
        deleteFields.innerHTML = `
            <label for="clanName">Clan Name:</label>
            <input type="text" id="clanName" name="clanName" placeholder="Enter Clan Name" required>
        `;
    } else if (action === "delete_guild") {
        deleteFields.innerHTML = `
            <label for="guildName">Guild Name:</label>
            <input type="text" id="guildName" name="guildName" placeholder="Enter Guild Name" required>
        `;
    } else if (action === "delete_weapon") {
        deleteFields.innerHTML = `
            <label for="weaponID">Weapon ID:</label>
            <input type="text" id="weaponID" name="weaponID" placeholder="Enter Weapon ID" required>
        `;
    }
});
