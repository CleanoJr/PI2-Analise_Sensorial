firebase.auth().onAuthStateChanged(user => {
    if (!user) {
        window.location.href = "../../painel_admin.html";
    }
})