// DELETE TASK
function deleteNote(noteId) {
    if (!confirm("Are you sure to delete this task?")) return;

    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        if (data.code === 200) {
            const row = document.getElementById("note-" + noteId);
            row.remove();
        } else {
            alert(data.message);
        }
    });
}

// TOGGLE DONE
function toggleDone(noteId) {
    fetch("/toggle-done", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        const row = document.getElementById("note-" + noteId);
        if (data.code === 200) {
            if (data.status) {
                row.classList.add("table-success");
            } else {
                row.classList.remove("table-success");
            }
        } else {
            alert(data.message);
        }
    });
}
